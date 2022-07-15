from tkinter import W
from PIL import Image, ImageDraw

def drawLayers(grlayers, col, row):
    
    w = 40*col
    h = 40*row
    
    img = Image.new("RGB", (w, h))
    draw = ImageDraw.Draw(img) 
    
    colorcount = 0
    color = ['green', 'red', 'yellow', 'blue']
    
    for gr in grlayers:    
        for idx_x in range(col):
            for idx_y in range(row):
                if gr.grid[idx_x][idx_y] != 0:
                    shape = [(30*idx_x, 30*idx_y), ((30*idx_x)+30, (30*idx_y)+30)]
                    draw.rectangle(shape, fill =color[colorcount])
        
        colorcount =+ 1
        
    
    # creating new Image object
    
    
    # create rectangle image 
    img.show()
    
   