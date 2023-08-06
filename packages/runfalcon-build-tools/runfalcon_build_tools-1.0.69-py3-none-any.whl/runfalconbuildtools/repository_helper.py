from runfalconbuildtools.file_utils import create_dir_if_not_exists, file_exists
from runfalconbuildtools.logger import Logger
from runfalconbuildtools.command_line_executor import CommandLineExecutor

class Repository:
    
    def __init__(self, url:str, branch:str):
        self.url = url
        self.branch = branch

class RepositoryHelper:

    executor:CommandLineExecutor = CommandLineExecutor()
    logger:Logger = Logger('RepositoryManager')

    def __init__(self, respository:Repository):
        self.repository = respository

    def create_clone_repo_script(self, outdir:str) -> str:
        script:str = '#!/bin/sh\n'
        script +=   'set -e\n'
        script +=   'git clone -b {branch} {repo_url} {out_dir}\n'.format(\
                    branch = self.repository.branch, \
                    repo_url = self.repository.url, \
                    out_dir = outdir)
        return script


    def get_source_artifacts(self, outdir:str = '.'):
        self.logger.info( \
            'Getting repository {repo}/{branch} to {outdir} ...'.format(repo = self.repository.url, branch = self.repository.branch, outdir = outdir))

        create_dir_if_not_exists(outdir)
        
        script:str = self.create_clone_repo_script(outdir)
        self.executor.execute_script(script)
        
        if self.executor.return_code != 0:
            raise Exception('Can\'t clone repository {repo}/{branch}.\nCode: {code}\n{cause}'.format(\
                repo = self.repository.url, \
                branch = self.repository.branch, \
                code = self.executor.return_code, \
                cause = self.executor.stderr))
