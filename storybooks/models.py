
from django.db import models
from django.utils import timezone

import os
from django.db.models.signals import post_delete
from django.dispatch import receiver

class Book(models.Model):
    title = models.CharField(max_length=255)
    cover_image = models.ImageField(upload_to='book_covers/', blank=False, null=True)
    pdf_file = models.FileField(upload_to='book_pdfs/', blank=True , null=True)
    description = models.TextField(blank =True)
    created_at = models.DateTimeField(default=timezone.now)  # แก้ตรงนี้
    updated_at = models.DateTimeField(auto_now=True)
    age_group = models.IntegerField(
        choices=[
                (3, "3 ปีขึ้นไป"),
                (4, "4-5 ปีขึ้นไป"),
                (6, "6-7 ปีขึ้นไป")
                ],
        default=3,
        help_text="ช่วงอายุที่เหมาะกับนิทาน"
    )
    double_page = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title

# NEW
@receiver(post_delete, sender=Book)
def delete_book_files(sender, instance, **kwargs):
    """ ลบไฟล์ PDF และ Cover Image ออกจากระบบเมื่อลบ Book """
    if instance.cover_image and instance.cover_image.storage.exists(instance.cover_image.name):
        instance.cover_image.storage.delete(instance.cover_image.name)

    if instance.pdf_file and instance.pdf_file.storage.exists(instance.pdf_file.name):
        instance.pdf_file.storage.delete(instance.pdf_file.name)

class Question(models.Model):

    Question_Type = (
        ("choice", "choice"),
        ("open", "open"),
    )
    
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="questions")
    type = models.CharField(
        max_length=20,
        choices=Question_Type,
        default="open"
    )
    question = models.CharField(
        max_length=255, default="", blank=False
    )
    options = models.JSONField(default=list)
    answer_index = models.IntegerField(default=0)  # ใช้ default=0
    page = models.IntegerField(default=1) 
    created_at = models.DateTimeField(default=timezone.now)  
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question  # แก้จาก self.text เป็น self.question
    

  