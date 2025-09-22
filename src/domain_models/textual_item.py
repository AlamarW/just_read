class TextualItem:
    def __init__(self, title: str, isbn: str):
        data = TextualItem._fetch_metadata(title, isbn)
        self.title = title
        self.isbn = isbn

    def _fetch_metadata(title: str ="", isbn: str=""):
        """Fetch metadata from an external source."""
        if not title and not isbn:
            raise ValueError
