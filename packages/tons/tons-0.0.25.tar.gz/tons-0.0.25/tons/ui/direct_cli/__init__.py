from ._commands._base_cmd import cli
from ._commands import _config_cmd
from ._commands import _keystore_cmd
from ._commands import _whitelist_cmd
from ._commands import _wallet_cmd
from ._commands import _contract_cmd
from ._commands import _dev_cmd


def main():
    cli()
