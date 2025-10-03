from django.db import models
from django.core.exceptions import ValidationError

class ReadingStatus(models.TextChoices):
    NOT_STARTED = "Not Started", "Not Started"
    IN_PROGRESS = "In Progress", "In Progress"
    COMPLETED = "Completed", "Completed"
    DNF = "Did Not Finish", "Did Not Finish"
    ON_HOLD = "On Hold", "On Hold"
    PLANNED = "Planned", "Planned"

class Reader(models.Model):
    name = models.CharField(max_length=200)
    active_project = models.ForeignKey(
        'ReadingProject', 
        null=True, 
        blank=True, 
        on_delete=models.SET_NULL,
        related_name='active_readers'
    )
    
    def add_project(self, name):
        project = ReadingProject.objects.create(name=name, reader=self)
        # Auto-set as active if no active project
        if not self.active_project:
            self.active_project = project
            self.save()
        return project
    
    def set_default_project(self, project=None):
        if self.readingproject_set.count() == 0:
            project = self.add_project(name="Default Reading Project")
        
        if project and project.reader != self:
            raise ValueError("Project not found in reader's projects")
        
        self.active_project = project
        self.save()
    
    @property
    def projects(self):
        return self.readingproject_set.all()

class ReadingProject(models.Model):
    name = models.CharField(max_length=200)
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def add_item(self, title, isbn, author):
        item = TextualItem.objects.create(
            title=title,
            isbn=isbn, 
            author=author,
            project=self
        )
        return item
    
    def delete_item(self, item):
        if item.project != self:
            raise ValueError("Item not in this project")
        item.delete()
    
    def total_project_pages(self):
        return self.textualitem_set.aggregate(
            total=models.Sum('total_pages')
        )['total'] or 0
    
    def total_books(self):
        return self.textualitem_set.filter(total_pages__gt=0).count()
    
    @property
    def items(self):
        return self.textualitem_set.all()

class TextualItem(models.Model):
    title = models.CharField(max_length=300)
    isbn = models.CharField(max_length=13)
    author = models.CharField(max_length=200)
    project = models.ForeignKey(ReadingProject, on_delete=models.CASCADE)
    
    progress_percent = models.DecimalField(max_digits=5, decimal_places=1, default=0)
    current_page = models.IntegerField(default=0)
    total_pages = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=ReadingStatus.choices, default=ReadingStatus.NOT_STARTED)
    rating = models.DecimalField(max_digits=2, decimal_places=1, null=True, blank=True)
    
    start_date = models.DateField(null=True, blank=True)
    completion_date = models.DateField(null=True, blank=True)
    dnf_date = models.DateField(null=True, blank=True)
    notes = models.JSONField(default=list, blank=True)
    
    def update_progress(self, current_page, total_pages):
        self.current_page = current_page
        self.total_pages = total_pages
        self.progress_percent = round((current_page / total_pages) * 100 if total_pages > 0 else 0, 1)
        
        if self.progress_percent == 100:
            self.status = ReadingStatus.COMPLETED
        elif self.progress_percent > 0:
            self.status = ReadingStatus.IN_PROGRESS
        else:
            self.status = ReadingStatus.NOT_STARTED
        
        self.save()
    
    def update_start_date(self, start_date):
        self.start_date = start_date
        self.save()
    
    def update_completion_date(self, completion_date):
        if self.status != ReadingStatus.COMPLETED:
            raise ValueError("Cannot set completion date unless status is COMPLETED")
        self.completion_date = completion_date
        self.save()
    
    def update_rating(self, rating):
        if rating < 1 or rating > 5:
            raise ValueError("Rating must be between 1 and 5")
        elif not (rating * 2).is_integer():
            raise ValueError("Rating must be of decimal values of .0 or .5")
        self.rating = rating
        self.save()