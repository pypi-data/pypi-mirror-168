

class NoDataException(Exception):
    def __init__(self, value):
        self.value = value
        
class ErrorDataException(Exception):
    def __init__(self, value):
        self.value = value
        
class CommandError(Exception):
    def __init__(self, value):
        self.value = value
        
        
class UnsupportPara(Exception):
    def __init__(self, value):
        self.value = value