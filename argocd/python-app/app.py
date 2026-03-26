from flask import Flask, request, render_template
import os

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["image"]
        if file:
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)
            return render_template("index.html", background=filepath)
    return render_template("index.html", background=None)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000);