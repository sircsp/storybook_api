from pdf2image import convert_from_path
import os

input_folder = 'pdf_raw'               # 👈 path ไปยังโฟลเดอร์ PDF ทั้งหมด
output_root = 'static/storybook_pages' # 👈 เก็บผลลัพธ์ไว้ใน static

os.makedirs(output_root, exist_ok=True)

pdf_files = [f for f in os.listdir(input_folder) if f.endswith('.pdf')]

for pdf_file in pdf_files:
    book_name = os.path.splitext(pdf_file)[0]
    output_folder = os.path.join(output_root, book_name)
    os.makedirs(output_folder, exist_ok=True)

    print(f'🔄 แปลง: {pdf_file} → {output_folder}')
    images = convert_from_path(os.path.join(input_folder, pdf_file), dpi=200)

    for i, image in enumerate(images):
        filename = os.path.join(output_folder, f'page_{i+1:02}.jpg')
        image.save(filename, 'JPEG')

    print(f'✅ {pdf_file} แปลงเสร็จแล้ว ({len(images)} หน้า) ✅\\n')