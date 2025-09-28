from domain_models.reading_project import ReadingProject

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