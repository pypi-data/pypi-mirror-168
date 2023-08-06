from array import array
from email.mime import application
from os import environ
from typing import Dict
from runfalconbuildtools.artifacts import Artifact, ArtifactsManager, DummyArtifact, JmeterArtifact, S3Artifact, LATEST_VERSION
from runfalconbuildtools.file_utils import copy_file, get_simple_file_name
from runfalconbuildtools.logger import Logger
from runfalconbuildtools.config_files_helper import ConfigFileHelper

class MainCommand:

    def __init__(self, command:str, operation:str, args:array = []):
        self.command = command
        self.operation = operation
        self.args = args

    def to_string(self) -> str:
        args:str = ' '
        for arg in self.args:
            args += '{key}="{value}" '.format(key = arg['key'], value = arg['value'])
        return self.command + ' ' + self.operation + args

    def get_argument(self, arg_name:str) -> Dict:
        filtered_args:array = list(filter(lambda arg : arg['key'] == arg_name, self.args))
        return filtered_args[0]['value'] if len(filtered_args) > 0 else None

    def get_args(self) ->array:
        return self.args

class ModuleMain:

    logger:Logger = Logger('ModuleMain')

    usage_message:str = \
                    'Use python -m runfalconbuildtools <command> <operation> [args..]\n\n' + \
                    'Commands:\n' + \
                    '\ts3-artifact: Access to runfalconbuildtools artifacts\n' + \
                    '\t\tOperations:\n' + \
                    '\t\t\tget: Download an specific artifact.  Arguments:\n' + \
                    '\t\t\t\tname=<artifact name>: Name of the artifact to download.\n' + \
                    '\t\t\t\tvresion=<version>: Artifact version to download\n' + \
                    '\t\t\t\toutdir=<output directory>: Directory where the artifact will be saved\n\n' + \
                    '\t\t\t\tExample: python -m runfalconbuildtools artifact get name="my-artifact" version="1.0.0" out="./my_artifact.zip"\n' + \
                    '\tconfig: Modify values in a file\n' + \
                    '\t\tOperations:\n' + \
                    '\t\t\tjson: Modify values in a json formatted file.  Arguments:\n' + \
                    '\t\t\t\tfile=<file path>: Path of the file to set values.\n' + \
                    '\t\t\t\t<arg_n>=<value_n>: <arg_n> is the name of the n json attribute.  If it is a nested attribute, each level should be separated by dot.\n' + \
                    '\t\t\tproperties: Modify values in a json formatted file.  Arguments:\n' + \
                    '\t\t\t\tfile=<file path>: Path of the file to set values.\n' + \
                    '\t\t\t\t<arg_n>=<value_n>: <arg_n> is the name of the n json attribute.  If it is a nested attribute, each level should be separated by dot.\n' + \
                    '\t\t\tdownload: Download configuration from runfalcon config repo.  Arguments:\n' + \
                    '\t\t\t\tapplication: Application owner of configuration\n' + \
                    '\t\t\t\tenv: Environment to configure.  Ejm: STAGE, PROD\n' + \
                    '\t\t\t\toutdir: Directory to save configuration files\n'

    def __init__(self, commnad_args:array):
        self.command_args = commnad_args

    def __create_arg(self, str_arg:str) -> Dict:
        index:int = str_arg.find('=')
        
        if index < 0:
            raise Exception('Invalid argument: {arg}\n\n{usage}'.format(arg = str_arg, usage = self.usage_message))

        key:str = str_arg[0:index]
        value:str = str_arg[index + 1 : len(str_arg)].strip()
        if value.startswith('"') and value.endswith('"'):
            value = value[1 : len(value) - 1]

        return {'key': key, 'value': value}

    def __get_command(self) -> MainCommand:
        if (self.command_args == None):
            raise Exception('No command args')

        if (len(self.command_args) < 2):
            raise Exception('Invalid comman.\n\n' + self.usage_message)

        args:array = []
        for arg in self.command_args[2:len(self.command_args)]:
            args.append(self.__create_arg(arg))

        main_command:MainCommand = MainCommand(self.command_args[0], self.command_args[1], args)
        return main_command

    def __get_s3_artifact(self, main_command:MainCommand):
        output_path:str = None
        artifact:Artifact = None

        out_dir:str = main_command.get_argument('outdir')
        if out_dir == None:
            raise Exception('Output directory not specified.\n\n' + self.usage_message)

        artifact_name:str = main_command.get_argument('name')
        if artifact_name == 'dummy':
            artifact = DummyArtifact()
        elif artifact_name == 'jmeter':
            artifact = JmeterArtifact()
        else:
            artifact = S3Artifact(artifact_name)

        artifacts_version = main_command.get_argument('version')
        if artifacts_version == None:
            artifacts_version = LATEST_VERSION

        artifact.version = artifacts_version

        artifacts_manager:ArtifactsManager = ArtifactsManager()
        output_path = artifacts_manager.get_artifact(artifact)
        copy_file(output_path, out_dir)
        simple_file_name:str = get_simple_file_name(output_path)

        self.logger.info('Artifact "{artifact}" version "{version}" successfully downloaded to "{out}"'
                        .format(artifact = artifact_name, version = artifacts_version, out = out_dir + '/' + simple_file_name))

    def __run_s3_artifact(self, main_command:MainCommand):
        if main_command.operation == 'get':
            self.__get_s3_artifact(main_command)

    def __get_config_file_generic_params(self, main_command:MainCommand) -> Dict:
        file = main_command.get_argument('file')
        if file == None:
            raise Exception('File not receive.\n\n' + self.usage_message)

        args:array = main_command.get_args()
        if args == None or len(args) < 2:
            raise Exception('No parameters to replace.\n\n' + self.usage_message)

        return {'file': file, 'args': args}

    def __config_file(self, main_command:MainCommand, type:str):
        config_file_generic_params:Dict = self.__get_config_file_generic_params(main_command)
        file_path:str = config_file_generic_params['file']
        args:array = config_file_generic_params['args']
        json_values:array = []
        for arg in args:
            if arg['key'] != 'file':
                json_values.append({arg['key']: arg['value']})

        config_file_helper:ConfigFileHelper = ConfigFileHelper()

        if type == 'json':
            config_file_helper.set_values_in_json_file(file_path, json_values, file_path)
        elif type == 'properties':
            config_file_helper.set_values_in_properties_file(file_path, json_values, file_path)

    def __download_config(self, main_command:MainCommand):
        application:str = main_command.get_argument('application')
        if application == None:
            raise Exception('application is required.\n\n' + self.usage_message)

        environment:str = main_command.get_argument('env')
        if environment == None:
            raise Exception('env is required.\n\n' + self.usage_message)

        outdir:str = main_command.get_argument('outdir')
        if outdir == None:
            raise Exception('outdir is required.\n\n' + self.usage_message)

        configuration_helper:ConfigFileHelper = ConfigFileHelper()
        configuration_helper.get_config_files_from_repo(application, environment, outdir)

    def __run_config(self, main_command:MainCommand):
        if main_command.operation == 'json' or main_command.operation == 'properties':
            self.__config_file(main_command, main_command.operation)
        elif main_command.operation == 'download':
            self.__download_config(main_command)

    def __run(self, main_command:MainCommand):
        if main_command.command == 's3-artifact':
            self.__run_s3_artifact(main_command)
        elif main_command.command == 'config':
            self.__run_config(main_command)

    def run(self):
        main_command:MainCommand = self.__get_command()
        self.__run(main_command)
