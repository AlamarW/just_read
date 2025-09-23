class ReadingStatus:
    NOT_STARTED = "Not Started"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    DNF = "Did Not Finish"
    ON_HOLD = "On Hold"
    PLANNED = "Planned"

class TextualItem:
    """
    A textual item is a book, article, paper, etc. that has been
    added to a user's reading project
    """
    def __init__(self, title: str, isbn: str, author: str, project_id):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.project_id = project_id
        self.progress_percent = 0
        self.current_page = 0
        self.total_pages = 0
        self.status = ReadingStatus.NOT_STARTED
        self.notes = []
        self.rating = None
    
    def update_progress(self, current_page: int, total_pages: int):
        self.current_page = current_page
        self.total_pages = total_pages
        self.progress_percent = (current_page / total_pages) * 100 if total_pages > 0 else 0
        if self.progress_percent == 100:
            self.status = ReadingStatus.COMPLETED
        elif self.progress_percent > 0:
            self.status = ReadingStatus.IN_PROGRESS
        else:
            self.status = ReadingStatus.NOT_STARTED
        

