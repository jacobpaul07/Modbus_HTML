class settingDTO():
    def __init__(self, IPAddress: str, Port: int,RegisterAddress: int, RegisterLength: int,RefreshTime: int):
        self.IPAddress = IPAddress
        self.Port = Port
        self.RegisterAddress = RegisterAddress
        self.RegisterLength = RegisterLength
        self.RefreshTime = RefreshTime