import sys
from runfalconbuildtools.main_module import ModuleMain

def run():
    module_main:ModuleMain = ModuleMain(sys.argv[1:len(sys.argv)])
    module_main.run()

run()