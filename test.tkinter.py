from tkinter import *

top = Tk()

c = Canvas(top, bg="white", height=600, width=1000)

coord = [100, 100, 100, 500, 600, 200, 300, 200]
polygon = c.create_polygon(coord, outline='black', fill='red', width=2)

c.pack(fill=BOTH, expand=1)
top.mainloop()