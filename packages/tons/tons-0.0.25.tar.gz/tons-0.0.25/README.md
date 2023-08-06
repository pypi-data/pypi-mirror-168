> WARNING: some commands may be upgraded or changed

# Functionality and examples

Easy installation with a single command for non developers
```bash
sh -c "$(curl -sSfL https://raw.githubusercontent.com/tonfactory/temp_tons_install/master/install)"
```

Installation with pip3
```bash
$ pip3 install tons
$ tons init
```
> WARNING: for better user experience use virtual environment (python3 -m venv venv & source venv/bin/activate)

tons encrypts all your wallets info in a keystore file using your password. Create an encrypted keystore and select it as a current keystore.

```bash
$ tons keystore new myKeystore
Password []:

$ tons config tons.keystore_name myKeystore
```


Create any type of a TON wallet

```bash
$ tons wallet create \
	PocketMoney \
	--workchain 0 \
	--version v4r2 \
	--comment “My main wallet” \
	--save-to-whitelist myPocketMoney
```


Add your contacts to a whitelist
```bash
$ tons whitelist add myBestFriend EQBP5aEPlmFNr4eS3DJw2ydC4X_hOumwZoqCcJgHVSQHjZWW
```


Transfer money from the wallet to a whitelist contact
```bash
$ tons transfer PockeyMoney myBestFriend 10 --message “Happy birthday!”
```


# Features


Switch between mainnet and testnet
```bash
$ tons config --network mainnet
```


Keystore, wallet, whitelist commands support CRUD (create, read, update, delete). Some examples

```bash
$ tons wallet get oldWallet
Raw address: 0:4fe5a10f96614daf8792dc3270db2742e17fe13ae9b0668a827098075524078d
Nonbounceable address: UQBP5aEPlmFNr4eS3DJw2ydC4X_hOumwZoqCcJgHVSQHjchT
Bounceable address: EQBP5aEPlmFNr4eS3DJw2ydC4X_hOumwZoqCcJgHVSQHjZWW
Version: v4r2
Workchain: 0
Comment: None

$ tons wallet delete oldWallet
Are you sure you want to delete oldWallet wallet? [y/N]: y

$ tons whitelist edit myBestFriend --name myFriend
``` 


Backup and restore your keystores

```bash
$ tons keystore backup ./myKeystore.backup
Password []: 
Backup stores keys in UNENCRYPTED FORM. Are you sure want to export unencrypted keys to disk? [y/N]: y

$ tons keystore restore myRestoredKeystore ./myKeystore.backup
Password []:
```

Export your wallet mnemonic words and import them in any official TON wallet

```bash
$ tons wallet reveal PocketMoney
Password []: 
cliff spin hawk artefact language volume subway surround nuclear lawn weird arrest mule cube impact crash abandon slender turn basic sentence actor you fix
```

Import wallet from mnemonic phrase 

```bash
$ tons wallet import-from-mnemonics restoredWallet v4r2 0 "cliff spin hawk artefact language volume subway surround nuclear lawn weird arrest mule cube impact crash abandon slender turn basic sentence actor you fix"
```

Export your wallet to .addr and .pk files

```bash
$ tons wallet to-addr-pk PocketMoney ./destinationDir/
Password []:
```

List all wallets and whitelist contacts with verbose information. Also, you can redirect output into a .md file to see a nice table.

```bash
$ tons wallet list --verbose
|   Name   | Version | WC |                     Address                      |       Comment        |  State   |    Balance    |
|:--------:|:-------:|:--:|:------------------------------------------------:|:--------------------:|:--------:|:-------------:|
|  PockeyMoney  |   v4r2  | 0  | EQBP5aEPlmFNr4eS3DJw2ydC4X_hOumwZoqCcJgHVSQHjZWW | None |  Active  | 1.095236369 |
|  Another wallet  |   v3r2  | 0  | EQCS9ZmXTu-VlDLIsjcQMpMjF0PSdA_aTD6MqCHlaLUoTARS |         None         |  Active  |  1.095236369  |

$ tons whitelist list -v  > myContacts.md
```

For daily usage you may prefer our tons-interactive version

```bash
$ tons-interactive
[✓] Pick command: Keystores
[✓] Pick command: Open keystore
[✓] Choose keystore to use: good.keystore
[?] Pick command: List wallets
 > List wallets
   Transfer
   Create wallet
   Init wallet
   Get wallet
   Edit wallet
   Delete wallet
   Reveal wallet mnemonics
   Import from mnemonics
   Wallet to .addr and .pk
   Backup keystore
   Back
```


# Development

A person can deploy smart-contracts using tons. There are three options: send-boc, send-internal, send-external.

**send-internal**
```bash
$ tons dev send-internal ./scripts/deploy.py deploy_through_internal MY_WALLET_NAME 0.1 --wait
```
 
```python
# ./scripts/deploy.py example. 
# Function must receive WalletContract and  return (str, Optional[Cell], Optional[Cell]) values.

from typing import Optional

from tonsdk.contract.wallet import WalletContract
from tonsdk.boc import Cell
from tonsdk.contract.token.ft import JettonMinter


def deploy_through_internal(wallet: WalletContract) -> (str, Optional[Cell], Optional[Cell]):
    minter = JettonMinter(admin_address=wallet.address,
                          jetton_content_uri="URL",
                          jetton_wallet_code_hex='CODE')

    return minter.address.to_string(), minter.create_state_init()["state_init"], None
```

**send-external**
```bash
$ tons dev send-external ./scripts/deploy.py deploy_through_external --wait
```

```python
# ./scripts/deploy.py example. 
# Function must receive nothing and return (str, Cell) values.
from tonsdk.contract.wallet import WalletContract, WalletVersionEnum, Wallets
from tonsdk.boc import Cell


def deploy_through_external() -> (str, Cell):
        wallet_workchain = 0
        wallet_version = WalletVersionEnum.v3r2
        wallet_mnemonics = "YOUR 24 ... WORDS".split(" ")

        _mnemonics, _pub_k, _priv_k, wallet = Wallets.from_mnemonics(
            wallet_mnemonics, wallet_version, wallet_workchain)
        return wallet.address.to_string(), wallet.create_init_external_message()["message"]
```

*Note: to deploy a wallet one can use '$ tons wallet WALLET_NAME init'*

**send-boc**
```bash
$ tons dev send-boc ./generated-through-fif.boc --wait
```

# Integrations

Example of automatic salary payment, you may use cron to run pay_salary.sh
```bash
$ cat employee.info
employee1 EQDvtizebIVTGYASXgjYX5sHfkGLW8aFTa7wfYCyARIpARB0 10
employee2 EQA-Ri7Oftdjq--NJmuJrFJ1YqxYk6t2K3xIFKw3syhIUgUe 20
employee3 EQCNLRRZkvoqAW6zwYyy_BVwOBcMnwqvyrSpm8WnACdzXuu3 15.5

$ cat pay_salary.sh
cd ~/team_workspace/ton/
source venv/bin/activate
tons config --local tons.keystore_name yandex

input="./employees.info"
while IFS= read -r line
do
    stringarray=($line)
    name=${stringarray[0]}
    addr=${stringarray[1]}
    salary=${stringarray[2]}

    tons wallet transfer SalaryWallet $name $salary --wait
done < "$input"
```