import json
import os
from typing import Dict, List, Optional, Tuple, Union
from pydantic import BaseModel, validator
from hashlib import sha256
from nacl.bindings import crypto_box_seed_keypair, crypto_box, crypto_box_open

from tons.tonsdk.crypto import generate_new_keystore, generate_keystore_key
from tons.tonsdk.utils import Address, InvalidAddressError
from tons.utils import storage
from tons.tonsdk.contract.wallet import WalletVersionEnum, Wallets
from ._exceptions import KeyStoreAlreadyExistsError, RecordAlreadyExistsError, \
    RecordDoesNotExistError, KeyStoreDoesNotExistError, InvalidKeyStoreError, \
    KeyStoreIsNotSpecifiedError, KeyStoreInvalidPasswordError


class TonCliBackupRecord(BaseModel):
    name: str
    comment: Optional[str] = ""
    config: str
    kind: str
    address: Union[str, Address]
    mnemonics: List[str]

    class Config:
        use_enum_values = True
        validate_assignment = True
        arbitrary_types_allowed = True

    def to_backup_record(self) -> Optional["BackupRecord"]:
        if not self.__supported_wallet():
            return None

        return BackupRecord(name=self.name, address=self.address,
                            version=self.__map_kind_to_version(), workchain=self.__map_config_to_workchain(),
                            mnemonics=" ".join(self.mnemonics), comment=self.comment)

    def __supported_wallet(self):
        return self.kind in self.kind_version_map.keys()

    def __map_kind_to_version(self):
        return self.kind_version_map[self.kind]

    def __map_config_to_workchain(self):
        # "wc=0,walletId=698983191,pk=qweqweqwe"
        return self.config.split(",")[0].split("=")[1]

    @property
    def kind_version_map(self) -> Dict:
        return {
            "org.ton.wallets.v2": WalletVersionEnum.v2r1,
            "org.ton.wallets.v2.r2": WalletVersionEnum.v2r2,
            "org.ton.wallets.v3": WalletVersionEnum.v3r1,
            "org.ton.wallets.v3.r2": WalletVersionEnum.v3r2,
        }


class BackupRecord(BaseModel):
    name: str
    address: Union[str, Address]
    version: WalletVersionEnum
    workchain: int
    mnemonics: str
    comment: Optional[str] = ""

    class Config:
        use_enum_values = True
        validate_assignment = True
        arbitrary_types_allowed = True

    @classmethod
    def from_record(cls, record: "Record", mnemonics: str) -> "BackupRecord":
        return cls(
            name=record.name,
            address=record.address,
            version=record.version,
            workchain=record.workchain,
            mnemonics=mnemonics,
            comment=record.comment,
        )


class Record(BaseModel):
    name: str
    address: Union[str, Address]
    version: WalletVersionEnum
    workchain: int
    public_key: str
    secret_key: str
    comment: Optional[str] = ""

    class Config:
        use_enum_values = True
        validate_assignment = True
        arbitrary_types_allowed = True

    @validator('address')
    def validate_address(cls, v, values, **kwargs):
        if v:
            if isinstance(v, Address):
                return v.to_string(False, False, False)

            try:
                addr = Address(v)
                return addr.to_string(False, False, False)

            except InvalidAddressError as e:
                raise ValueError(e)

    @property
    def address_to_show(self):
        return Address(self.address).to_string(True, True, True)


class KeyStore(BaseModel):
    filepath: str
    salt: str = ""
    public_key: str = ""
    version: int = 1
    records: List[Record] = []

    class Config:
        use_enum_values = True
        validate_assignment = True

    @classmethod
    def new(cls, filepath: str, password: str) -> 'KeyStore':
        data = generate_new_keystore(password)
        data["filepath"] = filepath
        return cls.parse_obj(data)

    @classmethod
    def load(cls, filepath) -> 'KeyStore':
        raw_data = storage.read_bytes(filepath)
        if len(raw_data) < 32:
            raise InvalidKeyStoreError(f"Broken keystore: {filepath}")

        hash_data = raw_data[:32]
        data = raw_data[32:]
        if hash_data != sha256(data).digest():
            raise InvalidKeyStoreError(f"Broken keystore: {filepath}")

        json_data = json.loads(data.decode('utf-8'))
        json_data["filepath"] = filepath

        return cls.parse_obj(json_data)

    def save(self):
        self.records = sorted(self.records, key=lambda record: record.name)
        json_data = json.dumps(self.dict(exclude={'filepath'})).encode('utf-8')
        hash_of_data = sha256(json_data).digest()
        storage.save_bytes(self.filepath, hash_of_data + json_data)

    def backup(self, filepath: str, password: str):
        backup_records = []
        for record in self.records:
            mnemonics = self.get_secret(record, password)
            backup_records.append(
                BackupRecord.from_record(record, mnemonics).dict())

        storage.save_json(filepath, backup_records)

    def get_record_by_name(self, name: str, raise_none: bool = False):
        return self.__get_record(name=name, raise_none=raise_none)

    def get_record_by_address(self, address: Union[str, Address], raise_none: bool = False):
        return self.__get_record(address=address, raise_none=raise_none)

    def edit_record(self, name: str, new_name: str, new_comment: str, save: bool = False):
        record = self.get_record_by_name(name, raise_none=True)
        record_idx = self.records.index(record)

        if new_name:
            self.records[record_idx].name = new_name

        if new_comment:
            self.records[record_idx].comment = new_comment

        if save:
            self.save()

    def delete_record(self, name: str, save: bool = False):
        record = self.get_record_by_name(name, raise_none=True)
        self.records.remove(record)

        if save:
            self.save()

    def add_record(self, name: str, address: Address, public_key: str,
                   mnemonics: List[str], version: WalletVersionEnum,
                   workchain: int, comment: Optional[str] = None,
                   password: Optional[str] = None, save=False) -> Record:
        if self.__get_record(name=name, address=address) is not None:
            raise RecordAlreadyExistsError(
                f"Record with the name '{name}' or address: '{address.to_string(True, True, True)}' already exists")

        key = (" ".join(mnemonics)).encode('utf-8')
        sk = self.__create_record_sk(key)

        new_record = Record(name=name, address=address,
                            version=version, workchain=workchain, comment=comment,
                            public_key=public_key, secret_key=sk.hex())

        self.records.append(new_record)

        if save:
            self.save()

    def get_secret(self, record: Record, password: str) -> str:
        src = bytes.fromhex(record.secret_key)
        nonce, public_key, data = src[:24], src[24:24+32], src[24+32:]

        pub_k, priv_k = generate_keystore_key(
            password, bytes.fromhex(self.salt))
        if pub_k != bytes.fromhex(self.public_key):
            raise KeyStoreInvalidPasswordError("Invalid keystore password.")

        decoded_key_bytes = crypto_box_open(data, nonce, public_key, priv_k)
        if not decoded_key_bytes:
            raise KeyStoreInvalidPasswordError("Invalid keystore password.")

        return decoded_key_bytes.decode("utf-8")

    def __create_record_sk(self, key: bytes) -> bytes:
        ephemeral_key_public, ephemeral_key_secret = crypto_box_seed_keypair(
            os.urandom(32))
        nonce = os.urandom(24)
        encrypted = crypto_box(key, nonce, bytes.fromhex(
            self.public_key), ephemeral_key_secret)

        return nonce + ephemeral_key_public + encrypted

    def __get_record(self, name: Optional[str] = None, address: Union[str, Address, None] = None,
                     raise_none: bool = False) -> Optional[Record]:
        record = None

        if name:
            record = next(
                (record for record in self.records if record.name == name), record)
            if record is None and raise_none:
                raise RecordDoesNotExistError(
                    f"Record with the name {name} does not exist")

        if address:
            address = address if isinstance(
                address, str) else address.to_string(False, False, False)
            record = next(
                (record for record in self.records if record.address == address), record)
            if record is None and raise_none:
                raise RecordDoesNotExistError(
                    f"Record with the address {address} does not exist")

        return record


class KeyStores:
    def __init__(self, keystores_workdir: str):
        self.keystores_workdir = keystores_workdir

        paths = storage.get_filenames_by_ptrn(
            keystores_workdir, "*.keystore")
        self.keystore_paths = {os.path.basename(path): path for path in paths}
        self._keystore_path = None

    def create_new_keystore(self, name: str, password: Optional[str] = None, save: bool = False) -> Tuple[KeyStore, str]:
        name = self.__keystore_name(name)

        if name in self.keystore_paths:
            raise KeyStoreAlreadyExistsError(
                f"Keystore with the name '{name}' already exists")

        if password is None:
            # TODO: generate password
            raise NotImplemented("Empty password is not supported")

        filepath = os.path.join(self.keystores_workdir, name)
        keystore = KeyStore.new(filepath=filepath, password=password)
        if save:
            keystore.save()

        self.keystore_paths[name] = keystore.filepath

        return keystore, password

    def get_keystore(self, keystore_name: Optional[str], raise_none: bool = False) -> Optional[KeyStore]:
        if keystore_name is None:
            raise KeyStoreIsNotSpecifiedError(
                "tons.keystore_name is not specified.")

        keystore_path = os.path.join(self.keystores_workdir, keystore_name)
        try:
            return KeyStore.load(keystore_path)

        except FileNotFoundError:
            if raise_none:
                raise KeyStoreDoesNotExistError(
                    f"Keystore with the name '{keystore_name}' does not exist.")

            return None

        except json.JSONDecodeError as e:
            raise InvalidKeyStoreError("Invalid keystore file. " + str(e))

    def restore_tons_keystore(self, name: str, filepath: str, password: Optional[str] = None):
        backup_records: List[BackupRecord] = []
        backup_raw_records = storage.read_json(filepath)
        for raw_record in backup_raw_records:
            backup_records.append(
                BackupRecord.parse_obj(raw_record))

        self.__restore_keystore(name, filepath, backup_records, password)

    def restore_ton_cli_keystore(self, name: str, filepath: str, password: Optional[str] = None):
        backup_records: List[BackupRecord] = []
        backup_ton_cli_raw_records = storage.read_json(filepath)
        for raw_record in backup_ton_cli_raw_records:
            backup_record = TonCliBackupRecord.parse_obj(
                raw_record).to_backup_record()
            if backup_record:
                backup_records.append(backup_record)

        self.__restore_keystore(name, filepath, backup_records, password)

    def __restore_keystore(self, name: str, filepath: str, backup_records: List[BackupRecord], password: Optional[str] = None):
        name = self.__keystore_name(name)

        keystore, _password = self.create_new_keystore(
            name, password, save=False)

        for backup_record in backup_records:
            mnemonics, pub_k, _priv_k, wallet = Wallets.from_mnemonics(
                backup_record.mnemonics.split(
                    " "), backup_record.version,
                backup_record.workchain)

            keystore.add_record(backup_record.name, wallet.address,
                                pub_k.hex(), mnemonics, backup_record.version,
                                backup_record.workchain, backup_record.comment,
                                save=False)
        keystore.save()

        self.keystore_paths[name] = keystore.filepath

    def __keystore_name(self, name):
        if not name.endswith(".keystore"):
            name += ".keystore"
        return name
