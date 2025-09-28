from src.domain_models.reading_project import ReadingProject

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