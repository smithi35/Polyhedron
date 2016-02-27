from tkinter import *

top = Tk()

c = Canvas(top, bg="white", height=720, width=1280)

coord = [100, 100, 100, 500, 600, 200, 300, 200]
# coord = [0,0,1280,720,1280,0,0,720]
polygon = c.create_polygon(coord, outline='black', fill='#135972125', width=2)
c.pack(fill=BOTH, expand=1)

# coord = [100, 100, 500, 500, 1000, 600]
# item = c.create_polygon(coord, outline='black', fill='#050050050', width=2)
# c.pack(fill=BOTH, expand=1)

top.mainloop()