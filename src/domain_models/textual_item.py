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
        self.rating = None
        self.start_date = None
        self.completion_date = None
        self.dnf_date = None
        self.notes = []
    
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
        