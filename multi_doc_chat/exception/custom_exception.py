import sys # gives access to Python runtime information
import traceback # helps us get the full stack trace of an exception in a readable format
from typing import Optional ,  cast

class DocumentPortalException(Exception) :  # Creates a custom exception class and Inherits from Python’s built-in Exception.
    def __init__(self, error_message , error_details : Optional[object] = None):
        # Normalize message
        if isinstance (error_message , BaseException) :  # Ensures that the error_message is always a string
            norm_msg = str(error_message)
        else : 
            norm_msg = str(error_message)
        """
        exc_type → type of exception (e.g., ZeroDivisionError)
        exc_value → the exception object itself
        exc_tb → traceback object (contains stack frames)
        """
        exc_type = exc_value = exc_tb = None

        if error_details is None : 
            exc_type , exc_value , exc_tb = sys.exc_info()

        else : 
            if hasattr (error_details , 'exc_info') : 
                exc_info_obj = cast(sys , error_details)
                exc_type , exc_value , exc_tb = exc_info_obj.exc_info()

            elif isinstance (error_details , BaseException): 
                exc_type , exc_value , exc_tb  = type(error_details) , error_details , error_details.__traceback__

            else : 
                exc_type, exc_value, exc_tb = sys.exc_info()

        last_tb = exc_tb
        while last_tb and last_tb.tb_next : last_tb = last_tb.tb_next # last frame is the exact place where the error actually occurred in your code.
        """
        last_tb → the last frame of the traceback (where the error happened).
        last_tb.tb_frame → the frame object, which contains info about that line of code.
        f_code.co_filename → the file name of the Python file where the error occurred.
        If last_tb doesn’t exist, it sets file_name to "<unknown>".
        """
        self.file_name = last_tb.tb_frame.f_code.co_filename if last_tb else " <unknown>"
        self.lineno = last_tb.tb_lineno if last_tb else -1 # This line finds the exact line in the file where the error happened.
        self.error_message = norm_msg


        if exc_type and exc_tb:
            self.traceback_str = ''.join(traceback.format_exception(exc_type, exc_value, exc_tb))
        else:
            self.traceback_str = ""

        super().__init__(self.__str__())


    def __str__(self):
        # Compact, logger-friendly message (no leading spaces)
        base = f"Error in [{self.file_name}] at line [{self.lineno}] | Message: {self.error_message}"
        if self.traceback_str:
            return f"{base}\nTraceback:\n{self.traceback_str}"
        return base

    def __repr__(self):
        return f"DocumentPortalException(file={self.file_name!r}, line={self.lineno}, message={self.error_message!r})"