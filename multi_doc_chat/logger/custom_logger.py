import os # work with files path and folder 
import logging # standard module for logging messages
import datetime # to get the current date and time 
import structlog # makes log structured in json format 

class CustomLogger : # create a custom logger that we can resuse in our code
    def __init__(self , log_dir = "logs") : 
        self.logs_dir = os.path.join(os.getcwd() , log_dir)  # joins folder names safely across different OS.
        os.makedirs(self.logs_dir ,  exist_ok=True) # create a log folder if does not exist
        log_file = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log" # log file name with the current timestamp
        # it ensure each run of the app has a new log

        self.log_file_path = os.path.join(self.logs_dir , log_file)

    def get_logger(self, name= __file__): # define the method to return a logger object 
        logger_name = os.path.basename(name) # only the file name from the full path

        # creates a handler to save logs in the file 
        file_handler = logging.FileHandler(self.log_file_path)
        file_handler.setLevel(logging.INFO) # only log INFO and above (WARNING, ERROR, CRITICAL).
        file_handler.setFormatter(logging.Formatter("%(message)s"))

        # creates a handler to save logs to the console (terminal)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO())
        console_handler.setFormatter(logging.Formatter("%(message)s"))


        # configure the python logging module to use both console and file handler 
        
        logging.basicConfig(
            level=logging.INFO,
            format="%(message)s",
            handlers=[console_handler , file_handler]
        )

        # Configures structlog (structured logging) to make JSON logs
        structlog.configure( # setup how logs will be handled and formatted 
            processors=[ # Processors are like steps our log goes through before it is finally written
                structlog.processors.TimeStamper(fmt="iso" , utc=True , key="timestamp"), # adds timestamp in ISO format.
                structlog.processors.add_log_level,
                structlog.processors.EventRenamer(to='event'), # renames the message field to "event"
                structlog.processors.JSONRenderer() # converts logs into JSON format
            ],
            logger_factory=structlog.stdlib.LoggerFactory(), # use python logging internally 
            cache_logger_on_first_use= True,

        )
        
        return structlog.get_logger(logger_name) # Returns a ready-to-use logger object
