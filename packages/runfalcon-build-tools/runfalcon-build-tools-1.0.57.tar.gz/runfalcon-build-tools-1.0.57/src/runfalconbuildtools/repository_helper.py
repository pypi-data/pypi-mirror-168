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


    def get_source_artifacts(self, outdir:str = '.'):
        self.logger.info( \
            'Getting repository {repo}/{branch} to {outdir} ...'.format(repo = self.repository.url, branch = self.repository.branch, outdir = outdir))
        
        self.executor.execute('git', [
                                    'clone',
                                    '-b', self.repository.branch,
                                    self.repository.url,
                                    outdir
                                    ]
                            )
        
        if self.executor.return_code != 0:
            raise Exception('Can\'t clone repository {repo}/{branch}.\nCode: {code}\n{cause}'.format(\
                repo = self.repository.url, \
                branch = self.repository.branch, \
                code = self.executor.return_code, \
                cause = self.executor.stderr))
