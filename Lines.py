class Lines:
    """
    Represents a line.
    """
    def __init__(self) -> None:
        pass

    def vline(self, x: float):
        """
        Vertical constant line `x = k`.
        """
        return lambda z : z*0 + x
    
    def hline(self, y: float):
        """
        Horizontal constant line `y = k`.
        """
        return lambda x : 0*x + y