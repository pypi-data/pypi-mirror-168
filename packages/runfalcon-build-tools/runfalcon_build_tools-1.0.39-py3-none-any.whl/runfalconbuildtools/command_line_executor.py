from array import array
from asyncio.log import logger
from runfalconbuildtools.file_utils import add_execution_permission_to_file, delete_file, create_file, get_runfalcon_tmp_file
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
        tmp_file = get_runfalcon_tmp_file('sh')
        create_file(tmp_file, script)
        add_execution_permission_to_file(tmp_file)
        self.execute(tmp_file)
        if delete:
            delete_file(tmp_file)
