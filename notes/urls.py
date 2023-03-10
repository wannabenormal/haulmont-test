from django.urls import path, include

from .views import (
    CreateUserView,
    LoginView,
    LogoutView,
    NotesView,
    NoteView,
    CreateNoteView,
    DeleteNoteView,
    UpdateNoteView
)

urlpatterns = [
    path('register/', CreateUserView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('notes/', NotesView.as_view()),
    path('notes/', include([
        path('create/', CreateNoteView.as_view()),
        path('<int:pk>/', NoteView.as_view()),
        path('<int:pk>/delete/', DeleteNoteView.as_view()),
        path('<int:pk>/update/', UpdateNoteView.as_view())
    ]))
]
