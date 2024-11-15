import base64

def get_base64_encoded_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

# Path to your image
image_path = 'C:\\Manasi\\NMIMS\\Manasi\\Capstone Project\\Agriculture\\Bhoomi\\Image\\bg.jpg'

# Get the base64 string
img_base64 = get_base64_encoded_image(image_path)
