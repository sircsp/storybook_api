from rest_framework import serializers
from .models import Book, Question
from rest_framework.parsers import MultiPartParser, FormParser


class BookSerializer(serializers.ModelSerializer):
    # cover_image = serializers.SerializerMethodField()
    # pdf_file = serializers.SerializerMethodField()
    cover_image = serializers.ImageField(required=False)  # รองรับการอัปโหลดไฟล์
    pdf_file = serializers.FileField(required=False)  # รองรับการอัปโหลดไฟล์

    class Meta:
        model = Book
        fields = ['id', 'title', 'cover_image','pdf_file', 'description'] 
    
    def to_representation(self, instance):
        """ แปลง URL ของไฟล์ให้เป็น Absolute URL """
        request = self.context.get('request', None)
        representation = super().to_representation(instance)

        if request:
            if instance.cover_image:
                representation['cover_image'] = request.build_absolute_uri(instance.cover_image.url)
            if instance.pdf_file:
                representation['pdf_file'] = request.build_absolute_uri(instance.pdf_file.url)

        return representation
    def get_cover_image(self, obj):
        if obj.cover_image and hasattr(obj.cover_image, 'url'):
            return self.context['request'].build_absolute_uri(obj.cover_image.url)
        return None

    def get_pdf_file(self, obj):
        request = self.context.get('request', None)
        if obj.pdf_file and hasattr(obj.pdf_file, 'url'):
            return self.context['request'].build_absolute_uri(obj.pdf_file.url)
        return None    

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'book', 'type', 'question', 'options', 'answer_index' ]
