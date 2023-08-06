import os
import stat
import shutil
import tempfile
from pathlib import Path
from runfalconbuildtools.string_util import get_random_string

def file_exists(file_path:str) -> bool:
    return os.path.exists(file_path)

def get_current_path():
    return os.path.dirname(os.path.abspath(__file__))

def delete_directory(dir_path:str):
    if file_exists(dir_path):
        shutil.rmtree(dir_path)

def create_file(file_path:str, content:str):
    with open(file_path, 'w') as f:
        f.write(content)

def add_execution_permission_to_file(file_path:str):
    st = os.stat(file_path)
    os.chmod(file_path, st.st_mode | stat.S_IEXEC)

def create_dir_if_not_exists(dir_path:str):
    if not file_exists(dir_path):
        os.makedirs(dir_path)

def delete_file(file:str):
    if os.path.exists(file):
        os.remove(file)

def get_tmp_dir() -> str:
    return tempfile.gettempdir()

def get_runfalcon_home() -> str:
    return os.path.expanduser("~") + '/.runfalcon'

def get_runfalcon_tmp_dir() -> str:
    rf_tmp_dir:str = get_runfalcon_home() + '/tmp'
    create_dir_if_not_exists(rf_tmp_dir)
    return rf_tmp_dir

def touch(file_path:str):
    Path(file_path).touch()

def get_runfalcon_tmp_file(ext:str = 'tmp'):
    tmp_dir:str = get_runfalcon_tmp_dir()
    file_name:str = tmp_dir + '/' + 'rf-' + get_random_string(15) + '.' + ext
    touch(file_name)
    return file_name

def copy_file(source:str, target:str):
    shutil.copy(source, target)

def move_file(source:str, target:str):
    if file_exists(target):
        delete_file(target)
    shutil.move(source, target)

def get_simple_file_name(full_file_name:str) -> str:
    arr = full_file_name.split('/')
    return arr[len(arr) - 1]

def copy_dir(source:str, target:str):
    if not file_exists(target):
        shutil.copytree(source, target)
    else:
        for root, dirs, files in os.walk(source, topdown=True):
            for name in files:
                copy_file(os.path.join(root, name), os.path.join(target, name))
            for name in dirs:
                copy_dir(os.path.join(root, name), os.path.join(target, name))
