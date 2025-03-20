# from django.urls import path
# from django.conf.urls.static import static
# from storybooks import views
# from storybooks.views import (
#     BookDetailView,
#     BookListView,
# )
# from django.conf import settings
# # from .views import update_question, delete_question
# from .views import (
#     BookDetailView, BookListView, create_book,
#     create_question, get_question_list, update_question, delete_question
# )
# from django.urls import path, include
# from django.contrib import admin

# urlpatterns = [
#     path("books/<int:pk>", BookDetailView.as_view(), name="book-detail"),
#     path("books", BookListView.as_view(), name="book-list"),
#     path("book", views.create_book, name="create-book"),
#     path("question/create", views.create_question, name="create-question"),
#     path("questions", views.get_question_list, name="question-list"),
#     # path("question/update", views.update_question, name="update-question"),
#     # path("question/delete", views.delete_question, name="delete-question"),
#     path('api/question/update/<int:question_id>/', update_question, name='update-question'),
#     path('api/question/delete/<int:question_id>/', delete_question, name='delete-question'),
    
# ]
# print("Loading storybooks.urls...")  # เพิ่มบรรทัดนี้ใน urls.py


# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)

from django.urls import path
from django.conf.urls.static import static
from storybooks import views
from storybooks.views import (
    BookDetailView,
    BookListView,
)
from django.conf import settings
from .views import (
    BookDetailView, BookListView, create_book,
    create_question, get_question_list, update_question, delete_question
)
from django.urls import path, include
from .views import get_questions_from_static

urlpatterns = [
    path("books/<int:pk>", BookDetailView.as_view(), name="book-detail"),
    path("books/", BookListView.as_view(), name="book-list"),
    path("book", views.create_book, name="create-book"),
    path("question/create", views.create_question, name="create-question"),
    path("questions", views.get_question_list, name="question-list"),
    path("question/update/<int:question_id>", update_question, name="update-question"),  
    path("question/delete/<int:question_id>", delete_question, name="delete-question"),
    path("static-questions/", get_questions_from_static, name="static-questions"),
]

print("Loading storybooks.urls...") 

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)

