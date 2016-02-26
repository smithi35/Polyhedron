from tkinter import *

top = Tk()

c = Canvas(top, bg="white", height=600, width=1000)

coord = [100, 100, 100, 500, 600, 200, 300, 200]
polygon = c.create_polygon(coord, outline='black', fill='#205205205', width=2)
c.pack(fill=BOTH, expand=1)

coord = [100, 100, 500, 500, 1000, 600]
item = c.create_polygon(coord, outline='black', fill='#050050050', width=2)
c.pack(fill=BOTH, expand=1)

top.mainloop()