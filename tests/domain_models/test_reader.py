from src.domain_models.reader import Reader

def test_add_project():
    reader = Reader(id=1, name="John Doe", active_project=None)
    project = reader.add_project(name="My Reading Project", project_id=1, reader_id=1)
    assert len(reader._projects) == 1
    assert reader._projects[0] == project
    assert project.name == "My Reading Project"
    assert project.reader_id == 1
    assert project.project_id == 1

def test_set_default_project():
    reader = Reader(id=1, name="John Doe", active_project=None)
    project1 = reader.add_project(name="Project 1", project_id=1, reader_id=1)
    project2 = reader.add_project(name="Project 2", project_id=2, reader_id=1)
    reader.set_default_project(project2)
    assert reader.active_project == project2

def test_initial_active_project():
    reader = Reader(id=1, name="John Doe", active_project=None)
    reader.set_default_project()
    assert reader.active_project.name == "Default Reading Project"