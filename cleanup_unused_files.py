import os
from django.core.wsgi import get_wsgi_application
import django

# ตั้งค่า Django Environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "my_project.settings")
# application = get_wsgi_application()
django.setup()

from storybooks.models import Book


# ตรวจสอบและสร้างโฟลเดอร์ media/ ก่อน
MEDIA_ROOT = "media"
if not os.path.exists(MEDIA_ROOT):
    os.makedirs(MEDIA_ROOT)

# กำหนดโฟลเดอร์สำหรับปกหนังสือและไฟล์ PDF
BOOK_COVERS_PATH = os.path.join(MEDIA_ROOT, "book_covers")
BOOK_PDFS_PATH = os.path.join(MEDIA_ROOT, "book_pdfs")

# ตรวจสอบและสร้างโฟลเดอร์ถ้ายังไม่มี
for path in [BOOK_COVERS_PATH, BOOK_PDFS_PATH]:
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"📁 Created directory: {path}")
    else:
        print(f"✅ Directory already exists: {path}")

# กำหนด Path ไปที่โฟลเดอร์ไฟล์มีเดีย
MEDIA_ROOT = "media/"
BOOK_COVERS_PATH = os.path.join(MEDIA_ROOT, "book_covers")
BOOK_PDFS_PATH = os.path.join(MEDIA_ROOT, "book_pdfs")

def cleanup_unused_files():
    """ ลบไฟล์ที่ไม่มีอยู่ในฐานข้อมูล """
    # ดึงรายชื่อไฟล์ที่ใช้จริงจาก Database
    used_covers = {book.cover_image.name for book in Book.objects.all() if book.cover_image}
    used_pdfs = {book.pdf_file.name for book in Book.objects.all() if book.pdf_file}

    # ลบไฟล์ปกหนังสือที่ไม่ได้ใช้
    for filename in os.listdir(BOOK_COVERS_PATH):
        file_path = os.path.join(BOOK_COVERS_PATH, filename)
        if f"book_covers/{filename}" not in used_covers and os.path.isfile(file_path):
            print(f"Deleting unused cover: {file_path}")
            os.remove(file_path)

    # ลบไฟล์ PDF ที่ไม่ได้ใช้
    for filename in os.listdir(BOOK_PDFS_PATH):
        file_path = os.path.join(BOOK_PDFS_PATH, filename)
        if f"book_pdfs/{filename}" not in used_pdfs and os.path.isfile(file_path):
            print(f"Deleting unused PDF: {file_path}")
            os.remove(file_path)

    print("Cleanup completed!")

if __name__ == "__main__":
    cleanup_unused_files()
