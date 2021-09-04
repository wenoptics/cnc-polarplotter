class Point:
    def __init__(self, x=0, y=0) -> None:
        self.x = x
        self.y = y

    @property
    def gcode(self):
        return f'X{self.x} Y{self.y}'

    def __str__(self) -> str:
        return f'({self.gcode})'
