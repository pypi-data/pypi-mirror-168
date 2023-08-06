from json import JSONDecodeError
import sys
from pydantic import ValidationError

from tons.config import ConfigNotFoundError
from .._utils import init_shared_object, setup_app
from ._utils import echo_error
from ._sets import EntrypointSet


def main():
    try:
        context = init_shared_object()
        setup_app(context.config)

    except (FileNotFoundError, JSONDecodeError, ConfigNotFoundError, ValidationError) as e:
        echo_error(e)

    if len(sys.argv) == 2 and sys.argv[1] == "--debug":
        context.debug_mode = True

    try:
        EntrypointSet(context).show()
    except KeyboardInterrupt:
        pass
