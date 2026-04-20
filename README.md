# Snap2PDF

Snap2PDF is a simple, modern, and lightweight web application built with Python Flask that allows you to instantly convert multiple images (JPG, JPEG, PNG) into a single PDF file. The entire process runs strictly in-memory, ensuring speed and absolute privacy—your files are never permanently saved to disk.

## Features
- **Batch Image Upload**: Select multiple images at once via file picker or drag-and-drop.
- **In-Memory Processing**: Conversions happen entirely in RAM without storing files temporarily or permanently.
- **Modern UI**: Clean, frictionless, and intuitive user interface built with HTML and vanilla CSS.
- **Smart Validation**: Gracefully handles incorrect format uploads, size constraints, and empty submissions.

## Tech Stack
- **Backend:** Python, Flask, Pillow (PIL)
- **Frontend:** HTML5, CSS3, Vanilla JavaScript

## Local Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Soutikkk/Snap2PDF.git
   cd Snap2PDF
   ```

2. Create and activate a Virtual Environment:
   ```bash
   python -m venv venv
   
   # For Windows Powershell / CMD
   venv\Scripts\activate
   
   # For macOS/Linux
   source venv/bin/activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   python app.py
   ```

The server will start on your local machine. You can view the app at `http://127.0.0.1:5000`.

## License
MIT License
