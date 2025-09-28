from src.models import Reader, ReadingProject, TextualItem, ReadingStatus
import pytest

def test_add_project():
    reader = Reader(id=1, name="John Doe", active_project=None)
    project = reader.add_project(name="My Reading Project", project_id=1, reader_id=1)
    assert len(reader._projects) == 1
    assert reader._projects[0] == project
    assert project.name == "My Reading Project"
    assert project.reader_id == 1
    assert project.project_id == 1

def test_set_default_project():
    reader = Reader(id=1, name="John Doe", active_project=None)
    project1 = reader.add_project(name="Project 1", project_id=1, reader_id=1)
    project2 = reader.add_project(name="Project 2", project_id=2, reader_id=1)
    reader.set_default_project(project2)
    assert reader.active_project == project2

def test_initial_active_project():
    reader = Reader(id=1, name="John Doe", active_project=None)
    reader.set_default_project()
    assert reader.active_project.name == "Default Reading Project"

def test_add_item():
    project = ReadingProject(name="My Reading Project", project_id=1, reader_id=1)
    item = project.add_item(title="Sample Book", isbn="1234567890", author="Author Name")
    assert item.project_id == 1
    assert len(project._items) == 1
    assert project._items[0] == item

def test_add_multiple_items():
    project = ReadingProject(name="My Reading Project", project_id=1, reader_id=1)
    item1 = project.add_item(title="Sample Book 1", isbn="1234567890", author="Author One")
    item2 = project.add_item(title="Sample Book 2", isbn="0987654321", author="Author Two")
    assert len(project._items) == 2
    assert project._items[0] == item1
    assert project._items[1] == item2

def test_get_items():
    project = ReadingProject(name="My Reading Project", project_id=1, reader_id=1)
    item1 = project.add_item(title="Sample Book 1", isbn="1234567890", author="Author One")
    item2 = project.add_item(title="Sample Book 2", isbn="0987654321", author="Author Two")
    items = project.get_items()
    assert len(items) == 2
    assert items[0] == item1
    assert items[1] == item2

def test_delete_item():
    project = ReadingProject(name="My Reading Project", project_id=1, reader_id=1)
    item1 = project.add_item(title="Sample Book 1", isbn="1234567890", author="Author One")
    item2 = project.add_item(title="Sample Book 2", isbn="0987654321", author="Author Two")
    project.delete_item(item1)
    assert len(project._items) == 1
    assert project._items[0] == item2

def test_total_project_pages():
    project = ReadingProject(name="My Reading Project", project_id=1, reader_id=1)
    item1 = project.add_item(title="Sample Book 1", isbn="1234567890", author="Author One")
    item2 = project.add_item(title="Sample Book 2", isbn="0987654321", author="Author Two")
    item1.update_progress(current_page=50, total_pages=200)
    item2.update_progress(current_page=100, total_pages=300)
    total_pages = project.total_project_pages()
    assert total_pages == 500

def test_total_project_pages_empty_project():
    project = ReadingProject(name="My Reading Project", project_id=1, reader_id=1)
    total_pages = project.total_project_pages()
    assert total_pages == 0

def test_total_books():
    project = ReadingProject(name="My Reading Project", project_id=1, reader_id=1)
    item1 = project.add_item(title="Sample Book 1", isbn="1234567890", author="Author One")
    item2 = project.add_item(title="Sample Book 2", isbn="0987654321", author="Author Two")
    item3 = project.add_item(title="Sample Book 3", isbn="1122334455", author="Author Three")
    item1.update_progress(current_page=50, total_pages=200)
    item2.update_progress(current_page=100, total_pages=300)
    total_books = project.total_books()
    assert total_books == 3

def test_total_books_empty_project():
    project = ReadingProject(name="My Reading Project", project_id=1, reader_id=1)
    total_books = project.total_books()
    assert total_books == 0

def test_update_progress():
    item = TextualItem(title="Sample Book", isbn="1234567890", author="Author Name", project_id=1)
    item.update_progress(current_page=50, total_pages=200)
    assert item.current_page == 50
    assert item.total_pages == 200
    assert item.progress_percent == 25.0
    assert item.status == ReadingStatus.IN_PROGRESS

def test_update_progress_rounded_percent():
    item = TextualItem(title="Sample Book", isbn="1234567890", author="Author Name", project_id=1)
    item.update_progress(current_page=31, total_pages=211)
    assert item.current_page == 31
    assert item.total_pages == 211
    assert item.progress_percent == 14.7
    assert item.status == ReadingStatus.IN_PROGRESS

def test_update_progress_to_completion():
    item = TextualItem(title="Sample Book", isbn="1234567890", author="Author Name", project_id=1)
    item.update_progress(current_page=200, total_pages=200)
    assert item.current_page == 200
    assert item.total_pages == 200
    assert item.progress_percent == 100.0
    assert item.status == ReadingStatus.COMPLETED

def test_update_progress_not_started():
    item = TextualItem(title="Sample Book", isbn="1234567890", author="Author Name", project_id=1)
    item.update_progress(current_page=0, total_pages=200)
    assert item.current_page == 0
    assert item.total_pages == 200
    assert item.progress_percent == 0.0
    assert item.status == ReadingStatus.NOT_STARTED

def test_update_completion_date():
    item = TextualItem(title="Sample Book", isbn="1234567890", author="Author Name", project_id=1)
    item.update_progress(current_page=200, total_pages=200)  # Mark as completed
    item.update_completion_date("2024-01-01")
    assert item.completion_date == "2024-01-01"

def test_update_completion_date_invalid_status():
    item = TextualItem(title="Sample Book", isbn="1234567890", author="Author Name", project_id=1)
    try:
        item.update_completion_date("2024-01-01")
    except ValueError as e:
        assert str(e) == "Cannot set completion date unless status is COMPLETED"
    else:
        assert False, "Expected ValueError was not raised"

def test_update_rating():
    item = TextualItem(title="Sample Book", isbn="1234567890", author="Author Name", project_id=1)
    item.update_rating(4)
    assert item.rating == 4

def test_update_rating_invalid():
    item = TextualItem(title="Sample Book", isbn="1234567890", author="Author Name", project_id=1)

    with pytest.raises(ValueError):
        item.update_rating(0)

def test_update_rating_only_half_values():
    item = TextualItem(title="Sample Book", isbn="1234567890", author="Author Name", project_id=1)

    with pytest.raises(ValueError):
        item.update_rating(3.4)

def test_update_rating_valid_half_value():
    item = TextualItem(title="Sample Book", isbn="1234123412", author="Author Name", project_id=1)
    item.update_rating(3.5)

    assert item.rating == 3.5