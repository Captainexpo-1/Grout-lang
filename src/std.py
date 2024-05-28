
class LangError(Exception):
    def __init__(self, message):            
            super().__init__(message)
            self.message = message
    def throw(self):
        # print in red color
        print("\033[91m",end="")
        print(self.message, end="")
        
        print("\033[0m",end="")
        exit(1)


def error(message, t="Parsing"):
    LangError(f"{t} error: {message}").throw()