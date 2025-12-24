"""Class representing an emmitter object"""


class Emitter:
    """Main goal of the emitter is produce the compiled code"""

    def __init__(self, fullpath):
        self.fullpath = fullpath
        self.header = ""
        self.code = ""

    def emit(self, code):
        """emits code"""

        self.code += code

    def emit_line(self, code):
        """Emits code line"""

        self.code += code + "\n"

    def header_line(self, code):
        """emits header code line"""

        self.header += code + "\n"

    def write_file(self):
        """Writes file to output"""

        with open(self.fullpath, "w") as output_file:
            output_file.write(self.header + self.code)
