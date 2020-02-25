from PIL import Image, ImageFont, ImageDraw
import os
import requests
from flask import Flask, render_template, request, send_file

@app.route("/")
def img_export():
    tile = request.form['tiles']
    
    image = Image.open('template.jpg')
    map1 = Image()

    new_height = int(map1.width*3431/1773)
    new_width = int(map1.height*3431/1773) 

    map2 = map1.resize((new_width,new_height),Image.ANTIALIAS)
    image_copy = image.copy()

    position = ((1715-(map2.width//2)),(1150-(map2.height//2)))
    image_copy.paste(map2,position)
    image_copy.save('abc2.jpg')
    image_copy.show()
    
if __name__ == "__main__":
    app.run(debug=True  )