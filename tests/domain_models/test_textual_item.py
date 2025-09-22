import pytest

from src.domain_models.textual_item import TextualItem

def test__fetch_metadata():
    title = ""
    isbn = ""

    with pytest.raises(ValueError):
        TextualItem(title, isbn)
