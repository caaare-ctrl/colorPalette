# One of my favourite websites to go to when I'm designing anything
# is a colour palette website called Flat UI Colors.
# It's a really simple static website that shows a bunch of colours and
# their HEX codes. I can copy the HEX codes and use it in my CSS or any design software.
# On day 76, you learnt about image processing with NumPy. Using this knowledge
# and your developer skills (that means Googling), build a website where a user
# can upload an image and you will tell them what are the top 10 most common colours in that image.
# This is a good example of this functionality:
# copy to clipboard
# https://www.w3schools.com/howto/howto_js_copy_clipboard.asp
# find color
# https://stackoverflow.com/questions/3241929/python-find-dominant-most-common-color-in-an-image
# https://towardsdatascience.com/color-identification-in-images-machine-learning-application-b26e770c4c71
import os
import numpy as np
from flask import Flask, render_template, request, url_for
from flask.cli import load_dotenv
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename, redirect
from form import ImageForm
from colorthief import ColorThief
from PIL import Image  # for reading image files
import matplotlib.colors as colors
from flask import send_from_directory


def rgb_to_hex(rgb_tuple):
    return colors.rgb2hex([1.0 * x / 255 for x in rgb_tuple])


load_dotenv(".env")

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SecretKey")
app.config["IMAGE_UPLOADS"] = 'static/img/'

Bootstrap(app)


@app.route("/", methods=["POST", "GET"])
def home():
    colors_example = ['#c3b6b7', '#9f1817', '#995f42', '#a97162', '#565a5d']
    form = ImageForm()
    if form.validate_on_submit():
        all_colors = []
        img = form.image.data
        img.save(os.path.join(app.config["IMAGE_UPLOADS"], img.filename))
        filename = "img/"+secure_filename(img.filename)
        color_thief = ColorThief(img)
        palette = color_thief.get_palette(color_count=5)
        for color in palette:
            all_colors.append(colors.rgb2hex(rgb_to_hex(color)))
        return redirect(url_for("color_page", imgcolor=all_colors, img= filename))

    return render_template("index.html", colors=colors_example, form=form)


@app.route("/colors")
def color_page():
    img = request.args.get("img")
    img_color = request.args.getlist("imgcolor")
    print(img)
    return render_template("colors.html", colors=img_color, img=img)


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == '__main__':
    app.run(port=3000, debug=True)
