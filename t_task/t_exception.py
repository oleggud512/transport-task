class TException(BaseException):
    def __init__(self, mes: str):
        self.mes = mes
