from rest_framework import serializers
from .models import Reader, ReadingProject, TextualItem

class TextualItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextualItem
        fields = ["title", "isbn", "author", "project", "progress_percent", "status", "total_pages"]

class ReadingProjectSerializer(serializers.ModelSerializer):
    items = TextualItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = ReadingProject
        fields = ["name", "created_at", 'items']
        read_only_fields = ["reader"]

class ReaderSerializer(serializers.ModelSerializer):
    projects = ReadingProjectSerializer(many=True, read_only=True)
    
    class Meta:
        model = Reader
        fields = ["name", "active_project", "projects"]