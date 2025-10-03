from rest_framework import serializers
from .models import Reader, ReadingProject, TextualItem

class TextualItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextualItem
        fields = ['id', 'title', 'isbn', 'author', 'total_pages', 'project']

class ReadingProjectSerializer(serializers.ModelSerializer):
    items = TextualItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = ReadingProject
        fields = ['id', 'name', 'created_at', 'reader', 'items']

class ReaderSerializer(serializers.ModelSerializer):
    projects = ReadingProjectSerializer(many=True, read_only=True)
    
    class Meta:
        model = Reader
        fields = ['id', 'username', 'email', 'active_project', 'projects']