from runfalconbuildtools.logger import Logger
from runfalconbuildtools.file_utils import delete_directory
from abc import ABC
from runfalconbuildtools.base_builder import BaseBuilder
from runfalconbuildtools.repository_helper import RepositoryHelper, Repository
from pathlib import Path

class AppBuilder(BaseBuilder, ABC):

    logger:Logger = Logger(Path(__file__).stem)

    def __init__(self, project_name:str, repo_url:str, branch:str):
        self.repo_url = repo_url
        self.branch = branch
        self.project_name = project_name

    def clean_output_directories(self):
        delete_directory(self.get_app_directory())
        delete_directory(self.get_build_file_dir())

    def get_source_artifacts(self):
        repository:Repository = Repository(self.repo_url, self.branch)
        repository_helper:RepositoryHelper = RepositoryHelper(repository)
        repository_helper.get_source_artifacts(self.get_app_directory())

    def get_app_name(self) -> str:
        return self.project_name
