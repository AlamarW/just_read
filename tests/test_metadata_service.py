import pytest
from src.metadata_service import MetadataService as MS

def test_fetch_metadata_no_values():
    title = ""
    isbn = ""

    with pytest.raises(ValueError):
        MS._fetch_metadata(title, isbn)

def test_fetch_metadata_with_title():
    title = "The Great Gatsby"
    isbn = ""  
    data = MS._fetch_metadata(title, isbn)

    assert data['numFound'] == 991
    assert data['docs'][0]['title'] == "The Great Gatsby"

def test_fetch_metadata_with_isbn():
    title = ""
    isbn = "9780743273565"  
    data = MS._fetch_metadata(title, isbn)

    assert data['numFound'] == 2
    assert data['docs'][0]['title'] == "The Great Gatsby"