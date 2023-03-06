class Cell:
    def __init__(self, val):
        self.value = val

    def set(self, val):
        if val > 255:
            self.value = val - 255
        elif val < 0:
            self.value = 256 + val
        else:
            self.value = val

class BrainF:
    def __init__(self, src):
        self.cells = [Cell(0)]
        self.cell_ptr = 0
        self.src_ptr = 0
        self.loops = []
        self.src = src

    def run(self):
        while self.src_ptr < len(self.src):
            self.parse_char()

    def parse_char(self):
        char = self.src[self.src_ptr]

        if char == '+':
            self.set_cell(1)
        elif char == '-':
            self.set_cell(-1)
        elif char == '>':
            self.set_ptr(1)
        elif char == '<':
            self.set_ptr(-1)
        elif char == '[':
            self.loops.append(self.src_ptr)
        elif char == ']':
            self.handle_loop()
        elif char == ".":
            self.output()
        elif char == ",":
            val = int(input("Input number: "))
            self.set_cell(val)

        self.src_ptr += 1

    def set_cell(self, val):
        cell = self.cells[self.cell_ptr]
        cell.set(cell.value + val)
        self.cells[self.cell_ptr] = cell

    def handle_loop(self):
        if self.cells[self.cell_ptr].value != 0:
            self.src_ptr = self.loops[-1]
        else:
            self.loops.pop()

    def set_ptr(self, val):
        self.cell_ptr += val

        if self.cell_ptr >= len(self.cells):
            self.cells.append(Cell(0))

    def output(self):
        val = self.cells[self.cell_ptr]
        print(chr(val.value))

    def __repr__(self):
        string = ""

        for cell in self.cells:
            string += f"{cell.value}, "

        return string

if __name__ == "__main__":
    source = input("Input brainfu*k code:\n")
    brainf = BrainF(source)
    brainf.run()
    print(brainf)