from nemonet.seleniumwebdriver.abstract_command import AbstractCommand
from nemonet.engines.graph import Action


class ReadAndStore(AbstractCommand):
    def execute_action(self, action: Action, driver):
        pass

    def command_name(self) -> str:
        return 'READ_AND_STORE'
