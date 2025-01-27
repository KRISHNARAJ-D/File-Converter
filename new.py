from pdf2image import convert_from_path
import os

def convert_pdf_to_images(pdf_path, output_folder=None, dpi=200, poppler_path=r"C:\Program Files\poppler-24.08.0\Library\bin"):
    """
    Convert PDF pages to images
    
    :param pdf_path: Path to the input PDF file
    :param output_folder: Folder to save images (default: same as PDF location)
    :param dpi: Resolution of the output images (default: 200)
    :param poppler_path: Path to the Poppler executables
    :return: List of paths to generated image files
    """
    # If no output folder specified, use PDF's directory
    if output_folder is None:
        output_folder = os.path.dirname(pdf_path)
    
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Base filename without extension
    base_filename = os.path.splitext(os.path.basename(pdf_path))[0]
    
    # Convert PDF to images
    images = convert_from_path(pdf_path, dpi=dpi, poppler_path=poppler_path)
    
    # Paths to save images
    image_paths = []
    
    # Save images
    for i, image in enumerate(images):
        image_path = os.path.join(output_folder, f'{base_filename}_page{i+1}.png')
        image.save(image_path, 'PNG')
        image_paths.append(image_path)
    
    return image_paths
