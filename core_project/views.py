from django.shortcuts import render
from rest_framework import viewsets
from .models import Reader, ReadingProject, TextualItem
from .serializers import ReaderSerializer, ReadingProjectSerializer, TextualItemSerializer

# Create your views here.
class ReadingProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ReadingProjectSerializer

    def get_queryset(self):
        queryset = ReadingProject.objects.all()
        reader_name = self.request.query_params.get('reader')

        if reader_name:
            queryset = queryset.filter(reader__name=reader_name)

        return queryset

    def perform_create(self, serializer):
        reader, _ = Reader.objects.get_or_create(name="Test User")
        serializer.save(reader=reader)

class TextualItemViewSet(viewsets.ModelViewSet):
    serializer_class = TextualItemSerializer

    def get_queryset(self):
        queryset = TextualItem.objects.all()
        project_id = self.request.query_params.get('project')

        if project_id:
            queryset = queryset.filter(project_id=project_id)

        return queryset