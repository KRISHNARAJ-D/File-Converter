import os
from flask import Flask, request, send_from_directory, render_template, send_file
from PyPDF2 import PdfMerger
from pdf2image import convert_from_path
from docx2pdf import convert as docx_convert
from PIL import Image

app = Flask(__name__)

# Set up the folder to save uploaded files and merged files
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Function to convert PDF to images
def convert_pdf_to_images(pdf_path, output_folder=None, dpi=200):
    if output_folder is None:
        output_folder = os.path.dirname(pdf_path)
    
    os.makedirs(output_folder, exist_ok=True)
    
    base_filename = os.path.splitext(os.path.basename(pdf_path))[0]
    images = convert_from_path(pdf_path, dpi=dpi)
    
    image_paths = []
    for i, image in enumerate(images):
        image_path = os.path.join(output_folder, f'{base_filename}_page{i+1}.png')
        image.save(image_path, 'PNG')
        image_paths.append(image_path)
    
    return image_paths

# Route to render the home page
@app.route('/')
def index():
    return render_template('index.html')

# Route for the PDF Merge page
@app.route('/pdf_merge')
def pdf_merge_page():
    return render_template('pdf_merge.html')

@app.route('/merge_pdf', methods=['POST'])
def merge_pdf():
    if 'pdf_files' not in request.files:
        return 'No file part'
    files = request.files.getlist('pdf_files')
    
    # Save the uploaded files temporarily
    pdf_paths = []
    for file in files:
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        pdf_paths.append(filename)
    
    # Merge the PDFs
    merged_pdf = os.path.join(app.config['UPLOAD_FOLDER'], 'merged_output.pdf')
    merger = PdfMerger()
    for pdf in pdf_paths:
        merger.append(pdf)
    merger.write(merged_pdf)
    merger.close()
    
    # Automatically trigger the download of the merged PDF
    return send_file(merged_pdf, as_attachment=True)

# Route for the PDF to Image page
@app.route('/pdf_to_img')
def pdf_to_img_page():
    return render_template('pdf_to_img.html')

@app.route('/pdf_to_img', methods=['POST'])
def pdf_to_img():
    if 'pdf_file' not in request.files:
        return 'No file part'
    
    # Save the uploaded PDF temporarily
    pdf_file = request.files['pdf_file']
    pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_file.filename)
    pdf_file.save(pdf_path)
    
    # Convert the PDF to images
    converted_images = convert_pdf_to_images(pdf_path, output_folder=app.config['UPLOAD_FOLDER'])
    
    # Return the first converted image as a download
    return send_from_directory(app.config['UPLOAD_FOLDER'], os.path.basename(converted_images[0]), as_attachment=True)

# Route for the Word to PDF page
@app.route('/word_to_pdf')
def word_to_pdf_page():
    return render_template('word_to_pdf.html')

@app.route('/word_to_pdf', methods=['POST'])
def word_to_pdf():
    if 'word_file' not in request.files:
        return 'No file part'
    file = request.files['word_file']
    
    # Save the uploaded file
    word_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(word_path)
    
    # Convert Word to PDF
    pdf_output = os.path.join(app.config['UPLOAD_FOLDER'], f"{os.path.splitext(file.filename)[0]}.pdf")
    try:
        docx_convert(word_path, pdf_output)
    except Exception as e:
        return f"Error converting Word to PDF: {e}"
    
    # Automatically trigger the download of the PDF
    return send_file(pdf_output, as_attachment=True)

# Route for the Image to PDF page
@app.route('/img_to_pdf')
def img_to_pdf_page():
    return render_template('img_to_pdf.html')

@app.route('/img_to_pdf', methods=['POST'])
def img_to_pdf():
    if 'image_files' not in request.files:
        return 'No file part'
    files = request.files.getlist('image_files')
    
    # Save the uploaded images temporarily
    image_paths = []
    for file in files:
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        image_paths.append(filename)
    
    # Convert the images to a single PDF
    pdf_output = os.path.join(app.config['UPLOAD_FOLDER'], 'output.pdf')
    image_list = []
    for image_path in image_paths:
        img = Image.open(image_path)
        img = img.convert('RGB')  # Convert to RGB if not already
        image_list.append(img)
    
    image_list[0].save(pdf_output, save_all=True, append_images=image_list[1:])
    
    # Automatically trigger the download of the PDF
    return send_file(pdf_output, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
