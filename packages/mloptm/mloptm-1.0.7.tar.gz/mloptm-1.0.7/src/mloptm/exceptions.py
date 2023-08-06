class NotOptimizedError(Exception):
    def __init__(self, message, errors=None):
        super().__init__(message)

        self.errors = errors

class NotConverganceError(Exception):
    def __init__(self, message, errors=None):
        super().__init__(message)

        self.errors = errors

class ParsingExpressionError(Exception):
    def __init__(self, message, errors=None):
        super().__init__(message)

        self.errors = errors

