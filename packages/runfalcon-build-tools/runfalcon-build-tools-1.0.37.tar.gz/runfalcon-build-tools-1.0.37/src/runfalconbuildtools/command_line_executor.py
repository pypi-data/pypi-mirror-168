from array import array
from asyncio.log import logger
from runfalconbuildtools.file_utils import add_execution_permission_to_file, delete_file, create_file
from runfalconbuildtools.logger import Logger
import subprocess
import tempfile

class CommandLineExecutor:

    logger:Logger = Logger('CommandLineExecutor')

    return_code:int = 0
    stdout:str = None
    stderr:str = None

    def execute(self, command:str, command_args:array = None):
        try:
            result = subprocess.run([command] + ([] if command_args == None else command_args), stdout=subprocess.PIPE)
            self.return_code = result.returncode
            self.stdout = result.stdout
            self.stderr = result.stderr
        except Exception as e:
            self.logger.error('Invoking process', e)
            self.return_code = -1
            self.stderr += '{curr}. {err}\n'.format(curr = self.stderr, err = str(e))

    def get_tmp_script_file_name() -> str:
        tempfile.TemporaryFile

    def execute_script(self, script:str, delete:bool = True):
        tmpFile = tempfile.NamedTemporaryFile(prefix='runfalcon-', suffix='.sh', delete=False)
        create_file(tmpFile.name, script)
        add_execution_permission_to_file(tmpFile.name)        
        self.execute(tmpFile.name)
        if delete:
            delete_file(tmpFile.name)
