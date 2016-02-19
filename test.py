from tkinter import *

top = Tk()

c = Canvas(top, bg="white", height=600, width=1000)
c.pack(fill=BOTH, expand=YES)

# vertices = [[0, -100, 0], [-100, 100, 0], [100, 100, 0], [0, 0, 200]]
coords = [100, 200, 500, 600]
c.create_line(coords)
coords = [600, 1000, 500, 500]
c.create_line(coords)


c.pack(fill=BOTH, expand=1)
top.mainloop()