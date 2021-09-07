import string
from typing import Mapping, Optional


class GCodeStatement:

    class GPart:
        """A part is like "X-10.25". """
        raw: str
        variable: str
        value: str

        def __init__(self, raw: str):
            self.raw = raw.strip()
            if not raw:
                return

            self.variable = raw[0]
            if self.variable not in string.ascii_uppercase:
                raise ValueError()
                
            self.value = raw[1:]

        def __str__(self):
            return self.raw

        def __repr__(self):
            return '{}<Var="{}" Value="{}">'.format(
                self.__class__.__name__,
                self.variable,
                self.value
            )

        def __eq__(self, other):
            if isinstance(other, self.__class__):
                return self.raw == other.raw
            return other == self.raw

    def __init__(self, cmd: GPart, args: Optional[Mapping[str, GPart]] = None):
        self.cmd = cmd
        self.args = args or {}

    def __str__(self):
        parts = [p.raw for p in self.args.values()]
        return f'{self.cmd.raw} {" ".join(parts)}'

    @classmethod
    def from_str(cls, raw: str):
        s = raw.split()
        # TODO Parse line number ("N")
        first = s[0]
        cmd = GCodeStatement.GPart(first)

        args = {}
        if len(s) > 1:
            for part in s[1:]:
                p = GCodeStatement.GPart(part)
                args[p.variable] = p

        return cls(cmd, args)


class GCodeLine:
    def __init__(self, statement: Optional[GCodeStatement] = None, comment: Optional[str] = None):
        self.statement = statement
        self.comment = comment

    def __str__(self):
        if self.statement is None:
            return ''
        return str(self.statement)

    @classmethod
    def from_str(cls, raw: str):
        comment = None

        # Parse ";" comments
        s = raw.split(';', 1)
        raw = s[0]
        if len(s) > 1:
            comment = s[1].strip()

        # Remove other comments, i.e. ( and %
        raw = raw.split('(', 1)[0]  # TODO
        raw = raw.split('%', 1)[0]
        raw = raw.strip()

        if not raw:
            raw = None
        else:
            raw = GCodeStatement.from_str(raw)

        return cls(raw, comment)


if __name__ == '__main__':
    # Some quick inline tests
    g = GCodeLine.from_str('G01 X21.194500 Y-125.353000 Z160 F25')
    print(g.statement, g.comment)

    g = GCodeLine.from_str('; Comments G01 X21.194500 Y-125.353000 Z160 F25')
    print(g.statement, g.comment)
