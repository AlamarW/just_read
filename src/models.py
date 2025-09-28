class Reader:
    def __init__(self, id, name, active_project):
        self.id = id
        self.name = name
        self.active_project = active_project
        self._projects = []

    def set_default_project(self, project=None):
        if len(self._projects) == 0:
            self.add_project(name="Default Reading Project", project_id=1, reader_id=self.id)
            project = self._projects[0]

        if project not in self._projects:
            raise ValueError("Project not found in reader's projects")
        self.active_project = project

    def add_project(self, name, project_id, reader_id):
        project = ReadingProject(name=name, project_id=project_id, reader_id=reader_id)
        self._projects.append(project)
        return project

class TextualItem:
    """
    A textual item is a book, article, paper, etc. that has been
    added to a user's reading project
    """
    def __init__(self, title: str, isbn: str, author: str, project_id: int=None):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.project_id = project_id
        self.progress_percent = 0
        self.current_page = 0
        self.total_pages = 0
        self.status = ReadingStatus.NOT_STARTED
        self.rating = None
        self.start_date = None
        self.completion_date = None
        self.dnf_date = None
        self.notes: list[str] = []
    
    def update_progress(self, current_page: int, total_pages: int):
        self.current_page = current_page
        self.total_pages = total_pages
        self.progress_percent = round((current_page / total_pages) * 100 if total_pages > 0 else 0, 1)
        if self.progress_percent == 100:
            self.status = ReadingStatus.COMPLETED
        elif self.progress_percent > 0:
            self.status = ReadingStatus.IN_PROGRESS
        else:
            self.status = ReadingStatus.NOT_STARTED

    def update_start_date(self, start_date):
        self.start_date = start_date

    def update_completion_date(self, completion_date): 
        if self.status == ReadingStatus.COMPLETED:
            self.completion_date = completion_date
        else:
            raise ValueError("Cannot set completion date unless status is COMPLETED")

    def update_rating(self, rating: int):
        if rating < 1 or rating > 5:
            raise ValueError("Rating must be between 1 and 5")
        elif not (rating * 2).is_integer():
            raise ValueError("Rating must be of decimal values of .0 or .5")
        self.rating = rating  

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
    
class ReadingStatus:
    NOT_STARTED = "Not Started"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    DNF = "Did Not Finish"
    ON_HOLD = "On Hold"
    PLANNED = "Planned"