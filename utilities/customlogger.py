# import logging
# import os
#
# class LogGen:
#     @staticmethod
#     def loggen():
#         log_dir = os.path.join(os.path.dirname(__file__), "Logs")  # Logs folder in utilities
#         log_file = os.path.join(log_dir, "automation.log")  # Path to log file
#
#         # Ensure the Logs directory exists
#         if not os.path.exists(log_dir):
#             os.makedirs(log_dir)
#
#         # Remove old handlers before setting new configuration
#         for handler in logging.root.handlers[:]:
#             logging.root.removeHandler(handler)
#
#         # Configure logging
#         logging.basicConfig(
#             filename=log_file,
#             format='%(asctime)s: %(levelname)s: %(message)s',
#             datefmt='%m/%d/%Y %I:%M:%S %p',
#             filemode='w'  # Overwrites log file instead of appending
#         )
#
#         logger = logging.getLogger()
#         logger.setLevel(logging.INFO)
#
#         # Force writing logs immediately
#         logger.info("Logger Initialized - Log file created")
#         return logger
#
# # 🔥 Test the Logger
# if __name__ == "__main__":
#     logger = LogGen.loggen()
#     logger.info("This is a test log message.")


import logging
import os

class LogGen:

    _initialized = False

    @staticmethod
    def loggen():

        log_dir = os.path.join(os.path.dirname(__file__), "Logs")
        log_file = os.path.join(log_dir, "automation.log")

        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

        # Clear file only once per execution
        if not LogGen._initialized:

            open(log_file, "w").close()

            file_handler = logging.FileHandler(log_file)

            formatter = logging.Formatter(
                "%(asctime)s: %(levelname)s: %(message)s",
                "%m/%d/%Y %I:%M:%S %p"
            )

            file_handler.setFormatter(formatter)

            logger.addHandler(file_handler)

            logger.info("Logger Initialized - Log file created")

            LogGen._initialized = True

        return logger