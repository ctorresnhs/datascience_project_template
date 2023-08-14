from dataclasses import dataclass
@dataclass
class Paths:
    project_log:str = "./project.log"
    path1: str = "n/a" 
@dataclass
class Folders:
    folder1: str = "n/a" 
@dataclass
class Params:
    project_name: str = "NEW DATASCIENCE PROJECT"

@dataclass
class Conf:
    paths:Paths = Paths()
    folders:Folders = Folders()
    params:Params = Params()

