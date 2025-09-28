import pytest
from src.models import Reader, ReadingProject, TextualItem, ReadingStatus

pytestmark = pytest.mark.django_db

def test_add_project():
    reader = Reader.objects.create(name="John Doe")
    project = reader.add_project(name="My Reading Project")
    assert reader.projects.count() == 1
    assert reader.projects.first() == project
    assert project.name == "My Reading Project"
    assert project.reader == reader

def test_set_default_project():
    reader = Reader.objects.create(name="John Doe")
    project1 = reader.add_project(name="Project 1")
    project2 = reader.add_project(name="Project 2")
    reader.set_default_project(project2)
    assert reader.active_project == project2

def test_initial_active_project():
    reader = Reader.objects.create(name="John Doe")
    reader.set_default_project()
    assert reader.active_project.name == "Default Reading Project"

def test_add_item():
    reader = Reader.objects.create(name="John Doe")
    project = reader.add_project(name="My Reading Project")
    item = project.add_item(title="Sample Book", isbn="1234567890", author="Author Name")
    assert item.project == project
    assert project.items.count() == 1
    assert project.items.first() == item

def test_add_multiple_items():
    reader = Reader.objects.create(name="John Doe")
    project = reader.add_project(name="My Reading Project")
    item1 = project.add_item(title="Sample Book 1", isbn="1234567890", author="Author One")
    item2 = project.add_item(title="Sample Book 2", isbn="0987654321", author="Author Two")
    assert project.items.count() == 2
    assert list(project.items.all()) == [item1, item2]

def test_delete_item():
    reader = Reader.objects.create(name="John Doe")
    project = reader.add_project(name="My Reading Project")
    item1 = project.add_item(title="Sample Book 1", isbn="1234567890", author="Author One")
    item2 = project.add_item(title="Sample Book 2", isbn="0987654321", author="Author Two")
    project.delete_item(item1)
    assert project.items.count() == 1
    assert project.items.first() == item2

def test_total_project_pages():
    reader = Reader.objects.create(name="John Doe")
    project = reader.add_project(name="My Reading Project")
    item1 = project.add_item(title="Sample Book 1", isbn="1234567890", author="Author One")
    item2 = project.add_item(title="Sample Book 2", isbn="0987654321", author="Author Two")
    item1.update_progress(current_page=50, total_pages=200)
    item2.update_progress(current_page=100, total_pages=300)
    total_pages = project.total_project_pages()
    assert total_pages == 500

def test_total_project_pages_empty_project():
    reader = Reader.objects.create(name="John Doe")
    project = reader.add_project(name="My Reading Project")
    total_pages = project.total_project_pages()
    assert total_pages == 0

def test_total_books():
    reader = Reader.objects.create(name="John Doe")
    project = reader.add_project(name="My Reading Project")
    item1 = project.add_item(title="Sample Book 1", isbn="1234567890", author="Author One")
    item2 = project.add_item(title="Sample Book 2", isbn="0987654321", author="Author Two")
    item3 = project.add_item(title="Sample Book 3", isbn="1122334455", author="Author Three")
    item1.update_progress(current_page=50, total_pages=200)
    item2.update_progress(current_page=100, total_pages=300)
    total_books = project.total_books()
    assert total_books == 3

def test_total_books_empty_project():
    reader = Reader.objects.create(name="John Doe")
    project = reader.add_project(name="My Reading Project")
    total_books = project.total_books()
    assert total_books == 0

def test_update_progress():
    reader = Reader.objects.create(name="John Doe")
    project = reader.add_project(name="My Reading Project")
    item = project.add_item(title="Sample Book", isbn="1234567890", author="Author Name")
    item.update_progress(current_page=50, total_pages=200)
    item.refresh_from_db()
    assert item.current_page == 50
    assert item.total_pages == 200
    assert float(item.progress_percent) == 25.0
    assert item.status == ReadingStatus.IN_PROGRESS

def test_update_progress_rounded_percent():
    reader = Reader.objects.create(name="John Doe")
    project = reader.add_project(name="My Reading Project")
    item = project.add_item(title="Sample Book", isbn="1234567890", author="Author Name")
    item.update_progress(current_page=31, total_pages=211)
    item.refresh_from_db()
    assert item.current_page == 31
    assert item.total_pages == 211
    assert float(item.progress_percent) == 14.7
    assert item.status == ReadingStatus.IN_PROGRESS

def test_update_progress_to_completion():
    reader = Reader.objects.create(name="John Doe")
    project = reader.add_project(name="My Reading Project")
    item = project.add_item(title="Sample Book", isbn="1234567890", author="Author Name")
    item.update_progress(current_page=200, total_pages=200)
    item.refresh_from_db()
    assert item.current_page == 200
    assert item.total_pages == 200
    assert float(item.progress_percent) == 100.0
    assert item.status == ReadingStatus.COMPLETED

def test_update_progress_not_started():
    reader = Reader.objects.create(name="John Doe")
    project = reader.add_project(name="My Reading Project")
    item = project.add_item(title="Sample Book", isbn="1234567890", author="Author Name")
    item.update_progress(current_page=0, total_pages=200)
    item.refresh_from_db()
    assert item.current_page == 0
    assert item.total_pages == 200
    assert float(item.progress_percent) == 0.0
    assert item.status == ReadingStatus.NOT_STARTED

def test_update_completion_date():
    reader = Reader.objects.create(name="John Doe")
    project = reader.add_project(name="My Reading Project")
    item = project.add_item(title="Sample Book", isbn="1234567890", author="Author Name")
    item.update_progress(current_page=200, total_pages=200)  # Mark as completed
    item.update_completion_date("2024-01-01")
    item.refresh_from_db()
    assert str(item.completion_date) == "2024-01-01"

def test_update_completion_date_invalid_status():
    reader = Reader.objects.create(name="John Doe")
    project = reader.add_project(name="My Reading Project")
    item = project.add_item(title="Sample Book", isbn="1234567890", author="Author Name")
    with pytest.raises(ValueError):
        item.update_completion_date("2024-01-01")

def test_update_rating():
    reader = Reader.objects.create(name="John Doe")
    project = reader.add_project(name="My Reading Project")
    item = project.add_item(title="Sample Book", isbn="1234567890", author="Author Name")
    item.update_rating(4)
    item.refresh_from_db()
    assert float(item.rating) == 4.0

def test_update_rating_invalid():
    reader = Reader.objects.create(name="John Doe")
    project = reader.add_project(name="My Reading Project")
    item = project.add_item(title="Sample Book", isbn="1234567890", author="Author Name")
    with pytest.raises(ValueError):
        item.update_rating(0)

def test_update_rating_only_half_values():
    reader = Reader.objects.create(name="John Doe")
    project = reader.add_project(name="My Reading Project")
    item = project.add_item(title="Sample Book", isbn="1234567890", author="Author Name")
    with pytest.raises(ValueError):
        item.update_rating(3.4)

def test_update_rating_valid_half_value():
    reader = Reader.objects.create(name="John Doe")
    project = reader.add_project(name="My Reading Project")
    item = project.add_item(title="Sample Book", isbn="1234123412", author="Author Name")
    item.update_rating(3.5)
    item.refresh_from_db()
    assert float(item.rating) == 3.5