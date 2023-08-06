from hashlib import new
import os
from collections import OrderedDict
import inquirer

from tons.tonclient.utils import Whitelist, KeyStoreInvalidPasswordError
from tons.tonsdk.contract.wallet import SendModeEnum, WalletVersionEnum, Wallets
from tons.utils import storage
from ._base import BaseSet
from .._modified_inquirer import TempText
from .._validators import number_bigger_than_zero, valid_mnemonics
from ..._utils import SharedObject, md_table
from .._utils import echo_success, echo_error
from tons.tonsdk.utils import Address


class KeystoreSet(BaseSet):
    def __init__(self, ctx: SharedObject, keystore_name: str) -> None:
        super().__init__(ctx)
        ctx.keystore = ctx.keystores.get_keystore(
            keystore_name, raise_none=True)
        ctx.whitelist = Whitelist(
            ctx.config.tons.whitelist_path)

    def _handlers(self) -> OrderedDict:
        ord_dict = OrderedDict()
        ord_dict["List wallets"] = self._handle_list_wallets
        ord_dict["Transfer"] = self._handle_transfer
        ord_dict["Create wallet"] = self._handle_create_wallet
        ord_dict["Init wallet"] = self._handle_init_wallet
        ord_dict["Get wallet"] = self._handle_get_wallet
        ord_dict["Edit wallet"] = self._handle_edit_wallet
        ord_dict["Delete wallet"] = self._handle_delete_wallet
        ord_dict["Reveal wallet mnemonics"] = self._handle_reveal_wallet_mnemonics
        ord_dict["Import from mnemonics"] = self._handle_import_from_mnemonics
        ord_dict["Wallet to .addr and .pk"] = self._handle_wallet_to_addr_pk
        ord_dict["Backup keystore"] = self._handle_backup_keystore
        ord_dict["Back"] = self._handle_exit
        return ord_dict

    def _handle_list_wallets(self):
        questions = [
            inquirer.Confirm(
                "verbose", message='Show verbose information?', default=True),
        ]
        verbose = self._prompt(questions)["verbose"]

        with self._processing():
            field_names = ['Name', 'Version', 'WC', 'Address', 'Comment']
            if verbose:
                field_names += ['State', 'Balance']

            wallets = self.ctx.keystore.records

            table = md_table()
            table.field_names = field_names
            if verbose:
                wallet_infos = self.ctx.ton_client.get_addresses_information(
                    [wallet.address for wallet in wallets])
                total = 0
                for wallet, wallet_info in zip(wallets, wallet_infos):
                    total += wallet_info.balance
                    table.add_row([wallet.name, wallet.version, wallet.workchain,
                                   wallet.address_to_show, wallet.comment,
                                   wallet_info.state, wallet_info.balance])
                if wallets:
                    table.add_row(["Total", "", "", "", "", "", total])
            else:
                for wallet in wallets:
                    table.add_row([wallet.name, wallet.version, wallet.workchain,
                                   wallet.address_to_show, wallet.comment])

        echo_success(table.get_string(), only_msg=True)

    def _handle_transfer(self):
        from_wallet = self.__select_wallet_or_false("Transfer from")
        if not from_wallet:
            return

        record = self.ctx.keystore.get_record_by_name(
            from_wallet, raise_none=True)

        to_contact = self.__select_contact_or_false("Send to")
        if not to_contact:
            return

        contact = self.ctx.whitelist.get_contact(to_contact, raise_none=True)

        questions = [
            inquirer.Text("amount", message='Amount in TON coins to transfer (set 0 to transfer all)',
                          validate=number_bigger_than_zero),
            inquirer.Confirm(
                "destroy_if_zero", message='Destroy if balance becomes zero?', default=False),
            inquirer.Text(
                "message", message='Message (press \'Enter\' to skip)'),
            inquirer.Confirm(
                "transfer_all", message='Transfer all?', default=False),
            inquirer.Confirm(
                "wait_for_result", message="Wait until transaction will be completed?", default=True),
        ]
        ans = self._prompt(questions)
        amount = float(ans["amount"])
        message = ans["message"]
        destroy_if_zero = ans["destroy_if_zero"]
        transfer_all = amount == 0
        wait_for_result = ans["wait_for_result"]
        send_mode = SendModeEnum.ignore_errors | SendModeEnum.pay_gas_separately
        if destroy_if_zero:
            send_mode |= SendModeEnum.destroy_account_if_zero
        if transfer_all:
            send_mode |= SendModeEnum.carry_all_remaining_balance

        mnemonics = self.__get_mnemonics(record)

        with self._processing():
            _mnemonics, _pub_k, _priv_k, wallet = Wallets.from_mnemonics(mnemonics, record.version,
                                                                         record.workchain)

            # always send money in one direction without bouncing
            result = self.ctx.ton_client.transfer(
                wallet, contact.address, amount, message, send_mode, False, wait_for_result)

        echo_success(str(result))

    def _handle_create_wallet(self):
        questions = [
            inquirer.List(
                "single", message="Choose option", choices=["Single", "Batch"],
                carousel=True),
        ]

        self._prompt(questions)
        questions = [
            inquirer.List(
                "single", message="Choose option", choices=["Single", "Batch"],
                carousel=True),
            inquirer.List(
                "version", message='Wallet version', choices=[e.value for e in WalletVersionEnum],
                carousel=True, default=self.ctx.config.tons.default_wallet_version),
            inquirer.Text(
                "workchain", message='Workchain', default="0"),
        ]
        ans = self._prompt(questions)
        is_single = ans["single"] == "Single"
        version = WalletVersionEnum(ans["version"])
        workchain = int(ans["workchain"])

        if is_single:
            questions = [
                inquirer.Text("name", message='Wallet name'),
                inquirer.Text(
                    "comment", message='Wallet description (leave blank to skip)'),
            ]
            ans = self._prompt(questions)
            name = ans["name"]
            comment = ans["comment"]
            questions = [
                inquirer.Text(
                    "contact_name", message='Enter name to save to whitelist (blank to skip)',
                    default=name),
            ]
            contact_name = self._prompt(questions)["contact_name"]

            wallets_to_create = [(name, comment, contact_name)]

        else:
            questions = [
                inquirer.Text("number_of_wallets",
                              message="Number of wallets to create"),
                inquirer.Text(
                    "prefix", message='Wallet name prefix (e.g. employee)'),
                inquirer.Text(
                    "comment", message='Overall wallets description (leave blank to skip)'),
                inquirer.Confirm(
                    "add_all_to_whitelist", message='Add all wallets to whitelist?', default=True),
            ]
            ans = self._prompt(questions)
            number_of_wallets = int(ans["number_of_wallets"])
            prefix = ans["prefix"] + "_"
            comment = ans["comment"]
            add_all_to_whitelist = ans["add_all_to_whitelist"]

            num_of_existing = sum(record.name.startswith(prefix)
                                  for record in self.ctx.keystore.records)
            existing_leading_zeros = len(str(num_of_existing))
            new_leading_zeros = len(str(number_of_wallets + num_of_existing))

            if new_leading_zeros != existing_leading_zeros:
                zeros_dif = new_leading_zeros - existing_leading_zeros
                replace_with = "_" + ("0" * zeros_dif)
                for record in self.ctx.keystore.records:
                    if record.name.startswith(prefix):
                        record.name = record.name.replace("_", replace_with)
                for contact in self.ctx.whitelist.contacts:
                    if contact.name.startswith(prefix):
                        contact.name = contact.name.replace("_", replace_with)

            wallets_to_create = []
            i = 1
            while len(wallets_to_create) < number_of_wallets:
                wallet_name_unique = False
                new_name = None
                contact_name = ""
                while not wallet_name_unique:
                    new_name = f"{prefix}{str(i).zfill(new_leading_zeros)}"
                    i += 1
                    if add_all_to_whitelist:
                        contact_name = new_name
                        if self.ctx.whitelist.get_contact(contact_name) is not None:
                            continue
                    if self.ctx.keystore.get_record_by_name(new_name) is not None:
                        continue
                    wallet_name_unique = True

                wallets_to_create.append(
                    (new_name, comment, contact_name))

        with self._processing():
            for wallet_name, comment, contact_name in wallets_to_create:
                if contact_name:
                    contact = self.ctx.whitelist.get_contact(contact_name)
                    if contact is not None:
                        raise Exception(
                            f"Contact with the name '{contact_name}' already exists")

                mnemonics, pub_k, _priv_k, wallet = Wallets.create(
                    version, workchain)
                self.ctx.keystore.add_record(wallet_name, wallet.address,
                                             pub_k.hex(), mnemonics, version,
                                             workchain, comment, save=False)

                if contact_name:
                    self.ctx.whitelist.add_contact(
                        contact_name, wallet.address.to_string(True), save=False)

            self.ctx.keystore.save()
            self.ctx.whitelist.save()

        echo_success()

    def _handle_init_wallet(self):
        wallet_name_to_init = self.__select_wallet_or_false("Wallet to init")
        if wallet_name_to_init == False:
            return
        questions = [
            inquirer.Confirm(
                "wait_for_result", message="Wait until transaction will be completed?", default=True),
        ]
        ans = self._prompt(questions)
        wait_for_result = ans["wait_for_result"]
        record = self.ctx.keystore.get_record_by_name(
            wallet_name_to_init, raise_none=True)
        mnemonics = self.__get_mnemonics(record)
        _mnemonics, _pub_k, _priv_k, wallet = Wallets.from_mnemonics(mnemonics, record.version,
                                                                     record.workchain)

        with self._processing():
            result = self.ctx.ton_client.deploy_wallet(wallet, wait_for_result)
        echo_success(str(result))

    def _handle_get_wallet(self):
        wallet_name = self.__select_wallet_or_false("Get wallet")
        if wallet_name == False:
            return

        wallet = self.ctx.keystore.get_record_by_name(
            wallet_name, raise_none=True)

        questions = [
            inquirer.Confirm(
                "verbose", message='Show balances?', default=True),
        ]
        verbose = self._prompt(questions)["verbose"]

        addr = Address(wallet.address)

        if verbose:
            addr_info = self.ctx.ton_client.get_address_information(
                wallet.address)

        echo_success(
            f"Raw address: {addr.to_string(False, False, False)}", True)
        echo_success(
            f"Nonbounceable address: {addr.to_string(True, True, False)}", True)
        echo_success(
            f"Bounceable address: {addr.to_string(True, True, True)}", True)
        echo_success(f"Version: {wallet.version}", True)
        echo_success(f"Workchain: {wallet.workchain}", True)
        echo_success(f"Comment: {wallet.comment}", True)

        if verbose:
            echo_success("--- Verbose wallet information ---", True)
            for k, v in addr_info.dict().items():
                echo_success(str(k) + ': ' + str(v), True)

    def _handle_edit_wallet(self):
        wallet_name = self.__select_wallet_or_false("Edit wallet")
        if wallet_name == False:
            return

        questions = [
            inquirer.Text(
                "new_name", message='New wallet name (leave blank to skip)'),
            inquirer.Text(
                "new_comment", message='New wallet description (leave blank to skip)'),
        ]
        ans = self._prompt(questions)

        new_name = ans["new_name"]
        new_comment = ans["new_comment"]

        self.ctx.keystore.edit_record(
            wallet_name, new_name, new_comment, save=True)

        echo_success()

    def _handle_delete_wallet(self):
        questions = [
            inquirer.List(
                "single", message="Choose option", choices=["Single", "Batch"],
                carousel=True),
        ]
        is_single = self._prompt(questions)["single"] == "Single"
        if is_single:
            wallet_name = self.__select_wallet_or_false("Delete wallet")
            if wallet_name == False:
                return
            confirm_phrase = f'Are you sure you want to delete {wallet_name} wallet?'
            names_to_delete = [wallet_name]

        else:
            questions = [
                inquirer.Text(
                    "prefix", message="Etner wallet prefix to delete (e.g. employee)"),
            ]
            prefix = self._prompt(questions)["prefix"] + "_"
            confirm_phrase = f'Are you sure you want to delete all wallets with {prefix} prefix?'
            names_to_delete = [
                record.name for record in self.ctx.keystore.records if record.name.startswith(prefix)]

        questions = [
            inquirer.Confirm(
                "is_sure", message=confirm_phrase, default=False, ),
            inquirer.Confirm(
                "delete_whitelist",
                message="Do you want to delete whitelist contacts with the same names?", default=False)
        ]
        ans = self._prompt(questions)
        is_sure = ans["is_sure"]
        delete_whitelist = ans["delete_whitelist"]

        if not is_sure:
            echo_success("Action canceled.", True)
            return

        for name in names_to_delete:
            self.ctx.keystore.delete_record(name, save=False)
            if delete_whitelist:
                self.ctx.whitelist.delete_contact(name, save=False)

        self.ctx.keystore.save()
        if delete_whitelist:
            self.ctx.whitelist.save()

        echo_success()

    def _handle_reveal_wallet_mnemonics(self):
        wallet_name = self.__select_wallet_or_false("Wallet to reveal")
        if wallet_name == False:
            return

        record = self.ctx.keystore.get_record_by_name(
            wallet_name, raise_none=True)
        mnemonics = " ".join(self.__get_mnemonics(record))
        echo_success(mnemonics)

    def _handle_import_from_mnemonics(self):
        mnemonic = self._prompt([TempText("mnemonics", message="Mnemonic words (splited by space)",
                                          validate=valid_mnemonics)])["mnemonics"].split(" ")

        questions = [
            inquirer.List(
                "version", message='Wallet version', choices=[e.value for e in WalletVersionEnum],
                carousel=True, default=self.ctx.config.tons.default_wallet_version),
            inquirer.Text(
                "workchain", message='Workchain', default="0"),
            inquirer.Text("name", message='Wallet name')
        ]
        ans = self._prompt(questions)
        version = WalletVersionEnum(ans["version"])
        workchain = int(ans["workchain"])

        mnemonics, pub_k, _priv_k, wallet = Wallets.from_mnemonics(
            mnemonic, version, workchain)

        name = self._prompt([inquirer.Text("name", message='Wallet name')])["name"]

        questions = [
            inquirer.Text(
                "comment", message='Wallet description (leave blank to skip)'),
            inquirer.Text(
                "contact_name", message='Enter name to save to whitelist (blank to skip)', default=name),
        ]
        ans = self._prompt(questions)
        comment = ans["comment"]
        contact_name = ans["contact_name"]

        if contact_name:
            contact = self.ctx.whitelist.get_contact(contact_name)
            if contact is not None:
                raise Exception(
                    f"Contact with the name '{contact_name}' already exists")

        self.ctx.keystore.add_record(name, wallet.address,
                                     pub_k.hex(), mnemonics, version,
                                     workchain, comment, save=True)

        if contact_name:
            self.ctx.whitelist.add_contact(
                contact_name, wallet.address.to_string(True), save=True)

        echo_success()

    def _handle_wallet_to_addr_pk(self):
        wallet_name = self.__select_wallet_or_false("Wallet to use")
        if wallet_name == False:
            return
        questions = [
            inquirer.Text("destination_dir",
                          message='Directory path to export into'),
        ]
        ans = self._prompt(questions)
        destination_dir = ans["destination_dir"]

        record = self.ctx.keystore.get_record_by_name(
            wallet_name, raise_none=True)
        mnemonics = self.__get_mnemonics(record)
        addr, pk = Wallets.to_addr_pk(mnemonics, record.version,
                                      record.workchain)
        addr_path = os.path.join(
            destination_dir, record.name + ".addr")
        pk_path = os.path.join(destination_dir, record.name + ".pk")
        storage.save_bytes(addr_path, addr)
        storage.save_bytes(pk_path, pk)
        echo_success()

    def _handle_backup_keystore(self):
        questions = [
            inquirer.Text("backup_file_path", message='Backup filepath'),
            inquirer.Confirm(
                "is_sure",
                message='Backup stores keys in UNENCRYPTED FORM. Are you sure want to export unencrypted keys to disk?',
                default=False),
            inquirer.Password("keystore_password",
                              message='Keystore password'),
        ]
        ans = self._prompt(questions)
        backup_file_path = ans["backup_file_path"]
        keystore_password = ans["keystore_password"]
        is_sure = ans["is_sure"]

        if not is_sure:
            echo_success("Action canceled.", True)
            return

        self.ctx.keystore.backup(
            backup_file_path, keystore_password)

        echo_success()

    def __select_wallet_or_false(self, message):
        if self.ctx.keystore.records:
            questions = [
                inquirer.List(
                    "wallet",
                    message=message,
                    choices=[record.name for record in self.ctx.keystore.records],
                    carousel=True
                )
            ]
            return self._prompt(questions)["wallet"]

        echo_success("You do not have any wallets yet.")
        return False

    def __select_contact_or_false(self, message):
        if self.ctx.whitelist.contacts:
            questions = [
                inquirer.List(
                    "contact",
                    message=message,
                    choices=[
                        record.name for record in self.ctx.whitelist.contacts],
                    carousel=True
                )
            ]
            return self._prompt(questions)["contact"]

        echo_success("You do not have any contacts yet.")
        return False

    def __get_mnemonics(self, record):
        while True:
            questions = [
                inquirer.Password("keystore_password", message='Keystore password'),
            ]
            keystore_password = self._prompt(questions)["keystore_password"]

            try:
                return self.ctx.keystore.get_secret(record, keystore_password).split(" ")
            except KeyStoreInvalidPasswordError as e:
                echo_error(str(e))
                continue
