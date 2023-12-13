from flask import Flask,request,render_template,redirect,url_for
import numpy as np
from PIL import Image

app=Flask(__name__)
app.app_context().push()
app.secret_key="aishadarvesh"

@app.route("/")
def home():
    return render_template("index.html")

def get_colors(image_path):
    global img
    # open the image using pillow
    img=Image.open(image_path)
    # resize the image for faster processing
    img.resize((100,100))
    # convert the image to numpy array
    img_array=np.array(img)
    # flatten the array to 1d array of pixels
    pixels=img_array.reshape(-1,3)
#     convert rgb to hex
    hex_colors=[]
    for pixel in pixels:
        hex_color='#%02x%02x%02x' % tuple(pixel)
        hex_colors.append(hex_color)
    # get most common top 10 colors from the image
    top_colors = list(set(hex_colors))[:26]
    return top_colors

@app.route("/image_to_color",methods=['POST','GET'])
def image_to_color():
    if request.method=="POST":
        file=request.files['image']
        if file:
            image_path="static/temp_img.jpeg"
            file.save(image_path)
            get_top_colors=get_colors(image_path)

            return render_template("color.html",get_top_colors=get_top_colors,image_path=image_path)
        return render_template("index.html")

if __name__=="__main__":
    app.run(debug=True)