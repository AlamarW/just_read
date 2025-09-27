from src.domain_models.reading_project import ReadingProject

def test_add_item():
    project = ReadingProject(name="My Reading Project", project_id=1, reader_id=1)
    item = project.add_item(title="Sample Book", isbn="1234567890", author="Author Name")
    assert item.title == "Sample Book"
    assert item.isbn == "1234567890"
    assert item.author == "Author Name"
    assert item.project_id == 1
    assert len(project._items) == 1
    assert project._items[0] == item