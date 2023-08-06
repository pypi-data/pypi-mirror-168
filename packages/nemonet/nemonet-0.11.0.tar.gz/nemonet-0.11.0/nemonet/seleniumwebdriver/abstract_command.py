import logging
logger = logging.getLogger(__name__)

import time
from abc import ABC, abstractmethod
from datetime import datetime
import uuid

from nemonet.engines.graph import Action
from nemonet.seleniumwebdriver.page_capture import PageCapturing
from nemonet.engines.cache_store import KeyValueStore

class AbstractCommand(ABC):

    @abstractmethod
    def execute_action(self, action: Action, driver):
        pass  # does nothing by default

    def execute(self, action: Action, driver, sleep_time=0.25, filename=None):
        """ Executes given action as a vision command """

        self.__sleep(sleep_time)
        self.__screenshot(action, driver)
        self.__log(str(action))
        self.execute_action(action, driver)
        self.__sleep(sleep_time)
        self.__screenshot(action, driver)
        self.__sleep(action.get_wait_after())

    def log(self, string):
        self.__log(string)

    def sleep(self, second):
        self.__sleep(second)

    def __screenshot(self, action, driver):
        """ Takes a screenshot of the current state of [ TERMINOLOGY ] using given driver
            and saves it as a .png file with given filename [ WHERE? ].
            Fails silently when given filename is None. """

        try:
            kv_store = KeyValueStore()
            value_true_false = kv_store.get_value_as_str("VISION_ENV_SCREENSHOTS")
            kv_store.close()

            if value_true_false.lower() == 'false':
                return
        except:
            logger.debug("Error KeyValue Store ", exc_info=True)

        if action == None:
            return

        if action.getElementType() == 'SCREENSHOT':
            return

        capture = PageCapturing(driver)
        now = datetime.now()
        filename = "screenshot_" + now.strftime("%Y%m%d-%H%M%S.%f") + "-" \
                   + action.getElementType() + "-" \
                   + str(uuid.uuid4()) + ".png"
        capture.capture_save(file_name_cpatured=filename)

    def __sleep(self, seconds):
        time.sleep(seconds)

    def __log(self, string):
        # TODO : recomputation should be avoided
        # set up
        # log
        logger.debug(string)
