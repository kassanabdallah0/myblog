from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import io
import os 

def create_test_image(filename="test_image.jpg", color=(73, 109, 137), size=(100, 100)):
    # Create an in-memory image using Pillow
    image = Image.new('RGB', size, color=color)
    img_io = io.BytesIO()
    image.save(img_io, format='JPEG')
    img_io.seek(0)
    return SimpleUploadedFile(filename, img_io.read(), content_type="image/jpeg")

def delete_test_image(image_path):
    if os.path.exists(image_path):
        os.remove(image_path)