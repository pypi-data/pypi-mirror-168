from abc import ABCMeta, abstractmethod
from collections import OrderedDict
import inquirer
from halo import Halo
import contextlib

from .._utils import echo_error, echo_success
from ..._utils import SharedObject
from .._modified_inquirer import ModifiedConsoleRender, ModifiedTheme, modified_prompt
from .._exceptions import EscButtonPressed


class BaseSet(metaclass=ABCMeta):
    MENU_KEY = "menu_option"

    def __init__(self, ctx: SharedObject) -> None:
        self.ctx = ctx
        self._exit = False
        self._spinner = Halo(text='Processing', spinner='dots')

    def show(self):
        while not self._exit:
            items = [
                inquirer.List(self.MENU_KEY, message="Pick command",
                              choices=self._handlers().keys(), carousel=True),
            ]

            try:
                item = self._prompt(items)[self.MENU_KEY]
            except (EscButtonPressed, KeyboardInterrupt) as e:
                self._handle_exit()
                continue

            try:
                self._handlers()[item]()
            except (EscButtonPressed, KeyboardInterrupt) as e:
                pass
            except Exception as e:
                if self.ctx.debug_mode:
                    raise

                echo_error(e.__repr__())

    def _prompt(self, questions):
        return modified_prompt(questions, render=ModifiedConsoleRender(theme=ModifiedTheme()),
                               raise_keyboard_interrupt=True)

    @abstractmethod
    def _handlers(self) -> OrderedDict:
        raise NotImplementedError

    def _handle_exit(self):
        self._exit = True

    def _start_loading(self):
        self._spinner.start()

    def _stop_loading(self):
        self._spinner.stop()

    @contextlib.contextmanager
    def _processing(self):
        try:
            self._start_loading()
            yield
        finally:
            self._stop_loading()
