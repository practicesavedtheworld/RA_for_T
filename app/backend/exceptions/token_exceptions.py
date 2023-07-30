class TokenGenerateAttemptFailed(Exception):
    def __str__(self):
        return """Token generation failed. It may caused
        because of wrong secret parameters or service is not available right now"""

    def __repr__(self):
        return self.__str__()
