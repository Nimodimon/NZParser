class NotFoundElementError(Exception):
    def __init__(self, elem=""):
        self.element = elem
        super().__init__(self.element)

    def __str__(self):
        return f"Element with name '{self.element}' not found"

class NotFoundPageError(Exception):
    def __init__(self, url=""):
        self.url = url
        super().__init__(self.url)

    def __str__(self):
        return f"Page by url '{self.url}' wasn`t found"

class NotAuthorizedError(Exception):
    def __init__(self, msg=""):
        self.message = msg
        super().__init__(self.message)

    def __str__(self):
        if self.message:
            return self.message
        return "You not authorized yet!"

class UnprocessableDataError(Exception):
    def __str__(self):
        return "Invalid data"

class InternalError(Exception):
    def __init__(self, msg=""):
        self.message = msg
        super().__init__(self.message)

    def __str__(self):
        if self.message:
            return self.message
        return f"Internal error occurred"

class UnsuccessfulLogin(Exception):
    def __str__(self):
        return "Login Failed: username or password is incorrect"
