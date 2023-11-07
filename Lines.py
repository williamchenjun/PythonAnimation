class Lines:
    def __init__(self) -> None:
        pass

    def vline(self, x: float):
        return lambda z : z*0 + x
    
    def hline(self, y: float):
        return lambda x : 0*x + y