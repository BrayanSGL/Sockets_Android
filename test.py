import tkinter as tk

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.canvas = tk.Canvas(self, width=400, height=400)
        self.canvas.pack()
        self.rect1 = self.canvas.create_rectangle(50, 50, 100, 100, fill="blue")
        self.rect2 = self.canvas.create_rectangle(150, 150, 200, 200, fill="red")
        self.animate()

    def animate(self):
        self.canvas.move(self.rect1, 2, 0)
        self.canvas.move(self.rect2, -2, 0)
        self.master.after(100, self.animate)

root = tk.Tk()
app = Application(master=root)
app.mainloop()