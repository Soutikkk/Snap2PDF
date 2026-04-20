from flask import Flask, render_template, request, send_file, flash, redirect, url_for
from PIL import Image
import io

app = Flask(__name__)
# Secret key is required for flashing messages
app.secret_key = 'super_secret_image_to_pdf_key'

# Limit the maximum allowed payload to 50 megabytes
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    """Check if the provided filename has an approved extension."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'images' not in request.files:
            flash('No files were found in the request.')
            return redirect(request.url)
        
        # Get the list of uploaded files
        files = request.files.getlist('images')
        
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if not files or files[0].filename == '':
            flash('No files selected. Please select at least one image.')
            return redirect(request.url)

        image_list = []
        
        # Process each uploaded file
        for file in files:
            if file and allowed_file(file.filename):
                try:
                    # Open the image file using Pillow from the in-memory stream
                    img = Image.open(file.stream)
                    
                    # Convert image to RGB format, as required for PDF saving
                    if img.mode != 'RGB':
                        img = img.convert('RGB')
                        
                    image_list.append(img)
                except Exception as e:
                    # Handle corrupted images or other processing errors
                    flash(f'Error processing file {file.filename}: {str(e)}')
                    return redirect(request.url)
            else:
                # Handle invalid file types
                flash(f'Invalid or unsupported format for {file.filename}. Allowed formats are: JPG, JPEG, PNG.')
                return redirect(request.url)
                
        # If we successfully processed images, convert to PDF
        if image_list:
            # We use io.BytesIO() to create the PDF entirely in memory
            # This avoids any permanent disk storage, as requested.
            pdf_bytes = io.BytesIO()
            
            # Save the first image, and append the remaining images to the same file
            image_list[0].save(
                pdf_bytes, 
                format='PDF', 
                save_all=True, 
                append_images=image_list[1:]
            )
            
            # Move the pointer to the beginning of the stream before sending
            pdf_bytes.seek(0)
            
            # Send the in-memory file as a downloadable attachment
            return send_file(
                pdf_bytes, 
                mimetype='application/pdf', 
                as_attachment=True, 
                download_name='converted_images.pdf'
            )
            
    # Render the upload form on GET request
    return render_template('index.html')

if __name__ == '__main__':
    # Run the Flask app
    app.run(debug=True)
