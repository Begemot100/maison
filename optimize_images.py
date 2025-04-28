import os
from PIL import Image

# Путь к папке с изображениями
folder_path = ('/Users/germany/PycharmProjects/PythonProject/PythonProject11/static/images/endo')

# Проходим по всем файлам в папке
for filename in os.listdir(folder_path):
    if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
        file_path = os.path.join(folder_path, filename)

        # Открываем картинку
        with Image.open(file_path) as img:
            # Уменьшаем размер (например, 80% от оригинала)
            img = img.resize((int(img.width * 0.8), int(img.height * 0.8)))

            # Сохраняем с оптимизацией (качество 80%)
            img.save(file_path, optimize=True, quality=80)

            print(f"✅ Оптимизировано: {filename}")

print("🎉 Все картинки успешно оптимизированы!")
