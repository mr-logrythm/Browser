import tkinter

WIDTH, HEIGHT = 800, 750
HSTEP, VSTEP = 15, 20
SCROLL_STEP = 100

class Browser:
    def __init__(self):
        self.window = tkinter.Tk()
        self.canvas = tkinter.Canvas(self.window, width=WIDTH, height=HEIGHT)
        self.canvas.pack()
        self.scroll = 0

    def layout(self, text):
        x_coordinate, y_coordinate = HSTEP, VSTEP
        display_list = []
        for char in text:
            display_list.append((x_coordinate, y_coordinate, char))
            x_coordinate += HSTEP
            if x_coordinate >= WIDTH - HSTEP:
                y_coordinate += VSTEP
                x_coordinate = HSTEP

        return display_list

    def write_text(self,text):
        layout_list = self.layout(text)
        self.canvas.delete("all")

        for x, y, c in layout_list:
            self.canvas.create_text(x, y - self.scroll, text=c)

    def scrolldown(self, e):
        self.scroll += SCROLL_STEP
