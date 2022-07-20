import io
from base64 import encodebytes
from PIL import Image
import os

def get_response_images():
    imgs_path = get_imgs_path()
    encoded_image = {}
    for path in imgs_path:
        file_name_with_extension = path.split('/').pop()
        file_name = file_name_with_extension.split('.')[0]
        img = get_image(path)
        encoded_image[file_name] = img

    return encoded_image

def get_image(image_path):
    pil_img = Image.open(image_path, mode='r')
    byte_arr = io.BytesIO()
    pil_img.save(byte_arr, format='PNG', quality=100)
    encoded_img = encodebytes(byte_arr.getvalue()).decode('ascii')

    return encoded_img

def get_imgs_path():
    directory = 'generated_files/images/'
    imgs_path = []
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        
        if os.path.isfile(f):
            imgs_path.append(f)

    return imgs_path
