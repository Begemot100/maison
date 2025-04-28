from PIL import Image
import os

input_folder = "/Users/germany/PycharmProjects/PythonProject/PythonProject11/static/images/portfolio"
output_folder = "/Users/germany/PycharmProjects/PythonProject/PythonProject11/static/images_webp/portfolio_webp"

os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(input_folder):
    if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        img = Image.open(os.path.join(input_folder, filename))
        output_file = os.path.join(output_folder, os.path.splitext(filename)[0] + '.webp')
        img.save(output_file, 'webp', quality=85)

print("✅ Все изображения конвертированы в WebP!")

