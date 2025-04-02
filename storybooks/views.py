from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, generics
from .models import Book, Question
from .serializers import BookSerializer, QuestionSerializer
from rest_framework.generics import UpdateAPIView
from .serializers import QuestionSerializer
from rest_framework.parsers import MultiPartParser, FormParser

import json
import os
from django.http import JsonResponse
from django.conf import settings
from django.core.management import call_command
from django.shortcuts import get_object_or_404
from django.http import HttpResponse

def test_host(request):
    return HttpResponse(f"Host: {request.get_host()}")

# class BookDetailView(APIView):
#     def get(self, request, pk):
#         try:
#             # book = Book.objects.get(pk=pk)  
#             book = get_object_or_404(Book, pk=pk)
#             # serializer = BookSerializer(book)
#             serializer = BookSerializer(book, context={'request': request})
#             return Response(serializer.data)
#         except Book.DoesNotExist:
#             return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)

class BookDetailView(APIView):
    parser_classes = (MultiPartParser, FormParser)  # รองรับ multipart/form-data

    def put(self, request, pk):
        parser_classes = (MultiPartParser, FormParser)
        try:
            book = Book.objects.get(pk=pk)
            serializer = BookSerializer(book, data=request.data, partial=True, context={'request': request})

            # ตรวจสอบและอัปเดตไฟล์
            if 'cover_image' in request.FILES:
                book.cover_image = request.FILES['cover_image']
            if 'pdf_file' in request.FILES:
                book.pdf_file = request.FILES['pdf_file']

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Book.DoesNotExist:
            return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)   
    # def put(self, request, pk):
    #     try:
    #         book = Book.objects.get(pk=pk)  
    #         serializer = BookSerializer(book, data=request.data, partial=True)
    #         if serializer.is_valid():
    #             serializer.save()
    #             return Response(serializer.data)
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #     except Book.DoesNotExist:
    #         return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)

    # class BookDetailView(APIView):


    def get(self, request, pk):
        try:
            # book = Book.objects.get(pk=pk)  
            book = get_object_or_404(Book, pk=pk)
            # serializer = BookSerializer(book)
            serializer = BookSerializer(book, context={'request': request})
            return Response(serializer.data)
        except Book.DoesNotExist:
            return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)
        
    def delete(self, request, pk):
        try:
            book = Book.objects.get(pk=pk)  
            book.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Book.DoesNotExist:
            return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)
        
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get(self, request, *args, **kwargs):
        return super(BookListView, self).get(request, *args, **kwargs)
    
@api_view(['POST'])
def create_book(request):
    serializer = BookSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def create_question(request):
    serializer = QuestionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()

        call_command('export_questions')

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_question_list(request):
    book_id = request.data.get("book_id") ###

    if book_id is None:
        return Response({'error': 'Book ID is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        questions = Question.objects.filter(book=book_id)
        serializer = QuestionSerializer(questions, many=True)

        call_command('export_questions')
        return Response(serializer.data)
    except Question.DoesNotExist:
        return Response({'error': 'Question not found'}, status=status.HTTP_404_NOT_FOUND)
@api_view(['GET'])
def get_questions_by_book(request):
    book_id = request.GET.get("book_id")

    if book_id is None:
        return Response({'error': 'book_id is required'}, status=status.HTTP_400_BAD_REQUEST)

    questions = Question.objects.filter(book_id=book_id)
    serializer = QuestionSerializer(questions, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PUT'])
# def update_question(request):
def update_question(request, question_id):
    try:
        question = Question.objects.get(id=question_id)
        serializer = QuestionSerializer(question, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Question.DoesNotExist:
        return Response({'error': 'Question not found'}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['DELETE'])
# def delete_question(request):
def delete_question(request, question_id):
    try: 
        question = Question.objects.get(id=question_id)
        question.delete()

        call_command('export_questions')
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Question.DoesNotExist:
        return Response({'error': 'Question not found'}, status=status.HTTP_404_NOT_FOUND)

# NEW   
class QuestionUpdateView(UpdateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

def get_questions_from_static(request):
    file_path = os.path.join(settings.BASE_DIR, "static", "questions.json")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
    except FileNotFoundError:
        return JsonResponse({"error": "File not found"}, status=404)
    

def get_book_pages(request, book_slug):
    folder = os.path.join(settings.BASE_DIR, 'static', 'storybook_pages', book_slug)
    if not os.path.exists(folder):
        return JsonResponse({"error": "not found"}, status=404)

    files = sorted(f for f in os.listdir(folder) if f.endswith('.jpg'))
    urls = [f'/static/storybook_pages/{book_slug}/{f}' for f in files]
    return JsonResponse(urls, safe=False)

def get_total_pages(request, slug):
    folder_path = os.path.join(settings.BASE_DIR, 'static', 'storybook_pages', slug)
    try:
        image_files = [f for f in os.listdir(folder_path) if f.endswith('.jpg')]
        image_files.sort()  # optional
        return JsonResponse({'total_pages': len(image_files)})
    except FileNotFoundError:
        return JsonResponse({'error': 'Not found'}, status=404)