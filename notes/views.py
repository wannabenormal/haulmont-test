from rest_framework import permissions, views, status
from rest_framework.generics import (
    CreateAPIView,
    RetrieveUpdateAPIView,
    ListAPIView,
    RetrieveAPIView,
    DestroyAPIView
)
from rest_framework.response import Response
from django.contrib.auth import get_user_model, login, logout

from .serializers import UserSerializer, LoginSerializer, NoteSerializer

from .models import Note


class CreateUserView(CreateAPIView):

    model = get_user_model()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = UserSerializer


class LoginView(views.APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request):
        serializer = LoginSerializer(
            data=self.request.data,
            context={'request': self.request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response(None, status=status.HTTP_202_ACCEPTED)


class LogoutView(views.APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):
        logout(request)
        return Response(None, status=status.HTTP_202_ACCEPTED)


class NotesView(ListAPIView):
    model = Note
    serializer_class = NoteSerializer

    def get_queryset(self):
        queryset = self.model.objects.filter(created_by=self.request.user)
        return queryset.order_by('-created_at')


class NoteView(RetrieveAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

    def get_queryset(self):
        queryset = Note.objects.filter(
            pk=self.kwargs['pk'],
            created_by=self.request.user
        )
        return queryset


class CreateNoteView(CreateAPIView):
    model = Note
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = NoteSerializer

    def perform_create(self, serializer):
        return serializer.save(created_by=self.request.user)


class UpdateNoteView(RetrieveUpdateAPIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = NoteSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        return Note.objects.filter(
            pk=self.kwargs['pk'],
            created_by=self.request.user
        )

    def put(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.created_by != request.user:
            raise PermissionError

        return self.partial_update(request, *args, **kwargs)


class DeleteNoteView(DestroyAPIView):
    serializer_class = NoteSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get_queryset(self):
        queryset = Note.objects.filter(
            pk=self.kwargs['pk'],
            created_by=self.request.user
        )
        return queryset
