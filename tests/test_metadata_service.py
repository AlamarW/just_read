import pytest
from src.metadata_service import MetadataService as MS

@pytest.mark.skip(reason="Requires network access to external API")
def test_fetch_metadata_no_values():
    title = ""
    isbn = ""

    with pytest.raises(ValueError):
        MS._fetch_metadata(title, isbn)

@pytest.mark.skip(reason="Requires network access to external API")
def test_fetch_metadata_with_title():
    title = "The Great Gatsby"
    isbn = ""  
    data = MS._fetch_metadata(title, isbn)

    assert data['numFound'] == 990
    assert data['docs'][0]['title'] == "The Great Gatsby"

@pytest.mark.skip(reason="Requires network access to external API")
def test_fetch_metadata_with_isbn():
    title = ""
    isbn = "9780743273565"  
    data = MS._fetch_metadata(title, isbn)

    assert data['numFound'] == 2
    assert data['docs'][0]['title'] == "The Great Gatsby"