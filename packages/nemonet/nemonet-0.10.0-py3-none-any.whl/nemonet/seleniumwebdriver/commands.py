'''
Created on 13 feb. 2018

@author: ex03210
'''
import configparser
import inspect
import logging
import sys
from importlib import import_module
from os import walk

logger = logging.getLogger(__name__)

from nemonet.seleniumwebdriver.command_list import *


class Command(object):
    """
        All kind of selenium actions and more
    """

    def __init__(self, driver=None):
        """Constructor"""
        self.driver = driver
        self._wait = WebDriverWait(self.driver, 60)
        # on construction, we need to provide the plugin commands
        try:
            self.build_plugins()
        except:
            logger.info("No plugins found")

    def executeSequences(self, seq, g):

        for step in g.getSetup():
            self.execute_command(step.getAction())

        pa = seq.get()
        for l in pa:
            # logger.info("Execute sequence=%s" % (str(l)))
            for el in l:
                a = g.getVertex(el).getAction()
                self.execute_command(a)

    def execute_command(self, action: Action):
        """
        TODO : error handling
        :param action:
        :return:
        """
        command_type = action.getElementType()

        try:
            command_class = commands[command_type]
            if (command_class == None):
                pass  # Dummy Command for testing purposes
            else:
                c = command_class()
                c.execute(action, self.driver)
                return c

        except KeyError:
            # TODO : AssertionError is too generic, in need of an UnknownCommandException
            logger.debug("Fatal Error KeyError ", exc_info=True)
            assert False, f"{command_type} is not a known command"

    def build_plugins(self):
        # use a configuration file approach
        config = configparser.ConfigParser()
        # is expected to have the cfg in the current folder
        config.read('vision.cfg')  # failure wrong name => KeyError
        # review this way of resolving the path to the plugin directory
        # config file needed to specify the path to the plugin folder
        mypath = config['PLUGIN']['PluginDir']
        vision_modules = []
        for (dirpath, dirnames, filenames) in walk(mypath):
            vision_modules.extend(filenames)
        filtered = list(filter(lambda vision_module: vision_module.startswith("vision_"), vision_modules))
        filtered = [w.removesuffix('.py') for w in filtered]
        # look for a plugin directory and determine the plugin package directory
        # example below retrieves instance of the module
        # maybe best is to add to config file
        classes_as_spec = []  # result classes after checking the class protocol
        for mod in filtered:
            m2 = import_module('.' + mod, package=config['PLUGIN']['PackageName'])

            # get the classes in the module
            classes = [cls_name for cls_name, cls_obj in inspect.getmembers(sys.modules[m2.__name__]) if
                       inspect.isclass(cls_obj)]

            # inspect what class has the correct method signature
            for cls in classes:
                is_vision_class = getattr(m2, cls)
                if hasattr(is_vision_class,
                           "execute_action") and is_vision_class.__base__.__name__ == 'AbstractCommand':
                    classes_as_spec.append(is_vision_class)
                    logger.info("Added plugin " + is_vision_class(self).command_name())
                    commands[is_vision_class(self).command_name()] = is_vision_class

# TODO : this variable is exposed and needs a better location
commands = {
    'DUMMY': None,
    'CLICKABLE': ClickableCommand,
    'CLICKABLE_DOUBLE': ClickableDoubleCommand,
    'TEXTABLE': TextableCommand,
    'JSexec': JSexecCommand,
    'SELECTABLE': SelectableCommand,
    'OPENURL': OpenURLCommand,
    'SCREENSHOT': ScreenshotCommand,
    'CLEARTEXTABLE': ClearTextableCommand,
    'CLEARTEXTABLETAB': ClearTextableTabCommand,
    'TEXTABLE-ENTER': TextableEnterCommand,
    'COMPAREPNG': ComparePNGCommand,
    'COMPAREPNGPHASH': ComparePNGHashCommand,
    'WAIT': WaitCommand,
    'SCROLLTOP': ScrollTopCommand,
    'SCROLLBOTTOM': ScrollBottomCommand,
    'TAB': TabCommand,
    'CLICKABLE_RIGHT': ClickableRightCommand,
    'DRAG_AND_DROP': DragAndDropCommand,
    'GOTO_FRAME': GoToFrameCommand,
    'SAVE_CURRENT_URL': SaveCurrentURLCommand,
    'SPLIT_STORED_URL': SplitStoredURLCommand,
    'FORMAT_STRINGS': FormatStringsCommand,
    'STORE_STRING': StoreStringCommand,
    'SITE_SETTINGS': SiteSettingsCommand,
    'TABS_AND_ENTER': TabsAndEnterCommand,
    'TABS_AND_TEXT': TabsAndTextCommand,
    'BROWSER_TABS_ADD': BrowserTabsAddCommand,
    'BROWSER_TABS_GOTO': BrowserTabsGoToCommand,
    'LOG_CURRENT_URL': LogCurrentURLCommand,
    'OPEN_STORED_URL': OpenStoredURLCommand,
    'BROWSER_TABS_GOTO_CURRENT': BrowserTabsGoToCurrentCommand,
    'TEXT_CURRENT_POSITION': TextCurrentPositionCommand,
    'TEXT_CURRENT_POSITION_STAMP': TextCurrentPositionStampCommand,
    'DRAG_AND_DROP_MOUSE': DragAndDropMouseCommand,
    'DRAG_AND_DROP_WITH_OFFSET': DragAndDropWithOffsetCommand,
    'SWITCH_TO_ALERT_AND_CONFIRM': SwitchToAlertAndConfirmCommand,
    'REMOVE_HTML_ELEMENT': RemoveHTMLElementCommand,
    'SPLIT_URL_AND_STORE': SplitURLAndStoreCommand,
    'SELECT_FROM_DROP_DOWN': SelectFromDropDownCommand,
    'SET_VISION_ENV': SetEnvironmentVariable,
    'SEL_EXISTS': SelectorExists,
    'GET_VALUE_AND_COMPARE': GetValueAndCompare
}
