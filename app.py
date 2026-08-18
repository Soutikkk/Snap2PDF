from flask import Flask, render_template, request, send_file, flash, redirect
from PIL import Image
import io

app = Flask(__name__)
app.secret_key = "secret-key"

# Maximum upload size: 50 MB
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}


def allowed_file(filename):
    """Return True if the file has an allowed extension."""
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


@app.route("/", methods=["GET", "POST"])
def index():

    # Show webpage normally
    if request.method == "GET":
        return render_template("index.html")

    # Get uploaded images
    files = request.files.getlist("images")

    if not files or files[0].filename == "":
        flash("Please select at least one image.")
        return redirect(request.url)

    images = []

    # Process every uploaded image
    for file in files:

        if not allowed_file(file.filename):
            flash(f"Invalid file: {file.filename}")
            return redirect(request.url)

        try:
            image = Image.open(file.stream)

            # PDF requires RGB images
            if image.mode != "RGB":
                image = image.convert("RGB")

            images.append(image)

        except Exception:
            flash(f"Could not process: {file.filename}")
            return redirect(request.url)

    # Create PDF in memory
    pdf = io.BytesIO()

    images[0].save(
        pdf,
        format="PDF",
        save_all=True,
        append_images=images[1:]
    )

    pdf.seek(0)

    # Send PDF to the user
    return send_file(
        pdf,
        mimetype="application/pdf",
        as_attachment=True,
        download_name="converted_images.pdf"
    )


if __name__ == "__main__":
    app.run(debug=True)
