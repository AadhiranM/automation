from utilities.logger import logger

class BaseTest:
    """Reusable base class for all tests."""

    def setup_method(self):
        logger.info(f"➡ STARTING: {self.__class__.__name__}")

    def teardown_method(self):
        logger.info(f"⬅ ENDING: {self.__class__.__name__}")
