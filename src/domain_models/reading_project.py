class ReadingProject:
    def __init__(self, name: str, reader_id: int):
        self.name = name
        self.reader_id = reader_id
        self._items: List[TextualItem] = []

    def add_item(self, title: str) -> TextualItem:
        item = TextualItem(title, self.id)
        self._items.append(item)
        return item

