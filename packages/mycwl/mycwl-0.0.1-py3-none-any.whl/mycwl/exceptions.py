class CWLLoginError(Exception):
    def __str__(self):
        return "Unable to form connection - please check credentials"

class CanvasCreationError(Exception):
    def __str__(self):
        return "Unable to create canvas - please double check inputs"