from flask import Flask, request, render_template
import cv2
import numpy as np
import os

app = Flask(__name__)

def cartoonify_image(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)
    edges = cv2.adaptiveThreshold(gray, 255,
                                  cv2.ADAPTIVE_THRESH_MEAN_C,
                                  cv2.THRESH_BINARY, 9, 9)
    color = cv2.bilateralFilter(img, 9, 250, 250)
    cartoon = cv2.bitwise_and(color, color, mask=edges)
    output_path = "static/cartoon.png"
    cv2.imwrite(output_path, cartoon)
    return output_path

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['image']
        path = os.path.join("static", "input.png")
        file.save(path)
        cartoon_path = cartoonify_image(path)
        return render_template('index.html', cartoon_image=cartoon_path)
    return render_template('index.html', cartoon_image=None)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
