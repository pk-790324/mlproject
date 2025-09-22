import os #for working with file paths & directories
import logging #Python’s built-in logging module (to track errors, info, warnings, etc.)
from datetime import datetime


LOG_FILE=f'{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log'
logs_path=os.path.join(os.getcwd(),'logs',LOG_FILE)
os.makedirs(logs_path,exist_ok=True)

"""
datetime.now() → current date and time
.strftime("%m_%d_%Y_%H_%M_%S") → formats it like 09_22_2025_08_15_33
Adds .log at the end
output:09_22_2025_08_15_33.log
So each time you run the script, you’ll get a new unique log file.
"""
"""
os.getcwd() → gives current working directory
os.path.join(..., 'logs', LOG_FILE) → builds a path like:/home/user/project/logs/09_22_2025_08_15_33.log
os.makedirs(..., exist_ok=True) → creates the folder (if it doesn’t exist already).
"""

LOG_FILE_PATH=os.path.join(logs_path,LOG_FILE)
#This makes sure the .log file is created inside the logs folder.



logging.basicConfig(
    filename=LOG_FILE_PATH,
    format='[%(asctime)s] %(lineno)d %(name)s - %(levelname)s -%(message)s',
    level=logging.INFO,
)

"""
filename=LOG_FILE_PATH → where logs are stored
format=... → defines how each log line looks
%(asctime)s → timestamp of the log
%(lineno)d → line number in the script where log happened
%(name)s → logger name (usually module name)
%(levelname)s → log level (INFO, ERROR, DEBUG, etc.)
%(message)s → actual log message
level=logging.INFO → minimum log level to capture (INFO and above)
"""

logging.info("Logging system initialized.")
logging.warning("This is just a warning message.")
logging.error("An error occurred in the program.")
