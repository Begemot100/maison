from PIL import Image
import os

input_folder = "/Users/germany/PycharmProjects/PythonProject/PythonProject11/static/images/teams"
output_folder = "/Users/germany/PycharmProjects/PythonProject/PythonProject11/static/teams_webp"

os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(input_folder):
    if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        img = Image.open(os.path.join(input_folder, filename))

        # Уменьшаем размер по ширине если нужно (например, максимум 1920px)
        max_width = 1920
        if img.width > max_width:
            height = int(max_width * img.height / img.width)
            img = img.resize((max_width, height), Image.LANCZOS)

        output_file = os.path.join(output_folder, os.path.splitext(filename)[0] + '.webp')

        # Сохраняем с нужным качеством (например 75)
        img.save(output_file, 'webp', quality=75, method=6)

print("✅ Все изображения оптимизированы и сохранены в формате WebP!")

