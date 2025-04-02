import os
from rest_framework import serializers
from .models import Book, Question
from rest_framework.parsers import MultiPartParser, FormParser


class BookSerializer(serializers.ModelSerializer):
    cover_image = serializers.ImageField(required=False)
    pdf_file = serializers.FileField(required=False)
    slug = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ['id', 'title', 'cover_image', 'pdf_file', 'description', 'age_group', 'double_page', 'slug']

    def to_representation(self, instance):
        request = self.context.get('request', None)
        representation = super().to_representation(instance)

        def fix_url(url):
            return url.replace('127.0.0.1', '10.0.2.2') if url else None

        if request:
            if instance.cover_image:
                url = request.build_absolute_uri(instance.cover_image.url)
                representation['cover_image'] = fix_url(url)
            if instance.pdf_file:
                url = request.build_absolute_uri(instance.pdf_file.url)
                representation['pdf_file'] = fix_url(url)

        return representation

    def get_cover_image(self, obj):
        if obj.cover_image and hasattr(obj.cover_image, 'url'):
            return self.context['request'].build_absolute_uri(obj.cover_image.url)
        return None

    def get_pdf_file(self, obj):
        if obj.pdf_file and hasattr(obj.pdf_file, 'url'):
            return self.context['request'].build_absolute_uri(obj.pdf_file.url)
        return None

    def get_slug(self, obj):  
        return os.path.splitext(os.path.basename(obj.pdf_file.name))[0]
    
class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'book', 'type', 'question', 'options', 'answer_index', 'page']