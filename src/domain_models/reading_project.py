from domain_models.textual_item import TextualItem

class ReadingProject:
    def __init__(self, name: str, project_id: int, reader_id: int):
        self.project_id = project_id
        self.name = name
        self.reader_id = reader_id
        self._items: list[TextualItem] = []

    def add_item(self, title: str, isbn: str, author: str):
        item = TextualItem(title, isbn, author)
        item.project_id = self.project_id
        self._items.append(item)
        return item

    def get_items(self):
        return self._items

    def delete_item(self, item: TextualItem):
        self._items.remove(item)
    
    def total_project_pages(self):
        return sum([item.total_pages for item in self._items if item.total_pages is not None])
    
    def total_books(self):
        return sum([1 for item in self._items if item.total_pages is not None])
    
