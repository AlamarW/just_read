import pytest

from src.domain_models.textual_item import TextualItem

def test_fetch_metadata_no_values():
    title = ""
    isbn = ""

    with pytest.raises(ValueError):
        TextualItem(title, isbn)

def test_fetch_metadata_with_title():
    title = "The Great Gatsby"
    isbn = ""  
    query = TextualItem(title, isbn)

    assert query.data['numFound'] == 991
    assert query.data['docs'][0]['title'] == "The Great Gatsby"

def test_fetch_metadata_with_isbn():
    title = ""
    isbn = "9780743273565"  
    query = TextualItem(title, isbn)
    print(query.data)
    assert query.data['numFound'] == 2
    assert query.data['docs'][0]['title'] == "The Great Gatsby"