from src.domain_models.textual_item import TextualItem
from src.domain_models.textual_item import ReadingStatus

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