import json
import os
from django.core.management.base import BaseCommand
from storybooks.models import Question
from django.conf import settings

class Command(BaseCommand):
    help = "Export all questions to a static JSON file"

    def handle(self, *args, **kwargs):
        # ดึงข้อมูลจากฐานข้อมูล
        questions = Question.objects.all().values("id", "book_id", "type", "question", "options", "answer_index")

        # ✅ แปลง QuerySet เป็น JSON-compatible
        data = []
        for q in questions:
            data.append({
                "id": q["id"],
                "book_id": q["book_id"],
                "type": q["type"],
                "question": q["question"],
                "options": json.loads(q["options"]) if isinstance(q["options"], str) else q["options"],  # ✅ แปลง JSON String เป็น List
                "answer_index": q["answer_index"]
            })

        # ✅ กำหนด path ไปที่ static
        static_dir = os.path.join(settings.BASE_DIR, "static")
        os.makedirs(static_dir, exist_ok=True)  # ✅ สร้างโฟลเดอร์ถ้ายังไม่มี

        file_path = os.path.join(static_dir, "questions.json")

        # ✅ เขียนลงไฟล์ JSON
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        self.stdout.write(self.style.SUCCESS(f"Successfully exported questions to {file_path}"))
