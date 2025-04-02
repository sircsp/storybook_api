from .views import test_host  
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
from .views import get_questions_by_book
from .views import get_total_pages

urlpatterns = [
    path("books/<int:pk>", BookDetailView.as_view(), name="book-detail"),
    path("books/", BookListView.as_view(), name="book-list"),
    path("book", views.create_book, name="create-book"),
    path("question/create", views.create_question, name="create-question"),
    path("questions/", get_questions_by_book, name="questions-by-book"),
    path("question/update/<int:question_id>", update_question, name="update-question"),  
    path("question/delete/<int:question_id>", delete_question, name="delete-question"),
    path("static-questions/", get_questions_from_static, name="static-questions"),
    path("testhost/", test_host),
    path('books/<slug:slug>/pages/', get_total_pages),
]

print("Loading storybooks.urls...") 

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)

