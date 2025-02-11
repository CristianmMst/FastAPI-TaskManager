from fastapi.param_functions import Form


class OAuth2EmailRequestForm:
    def __init__(self, email: str = Form(...), password: str = Form(...)):
        self.email = email
        self.password = password
