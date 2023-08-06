from abc import ABC, abstractmethod
from enum import Enum
from runfalconbuildtools.file_utils import get_runfalcon_tmp_dir
from runfalconbuildtools.command_line_executor import CommandLineExecutor
from runfalconbuildtools.logger import Logger
from runfalconbuildtools.properties import Properties

LATEST_VERSION:str = 'latest'
UNKNOWN:str = 'unknown'

class Artifact(ABC):
    
    def __init__(self, name:str, type:str):
        self.name = name
        self.type = type

class S3ArtifactMetadata:

    def __init__(self, folder:str, name:str, latest_version:str, type:str):
        self.folder = folder
        self.name = name
        self.latest_version = latest_version
        self.type = type

    def to_simple_file_name(self) -> str:
        return  self.name + \
                ('-' + self.latest_version if self.latest_version != None and self.latest_version != LATEST_VERSION else '') + \
                '.' + (self.type if self.type != None else UNKNOWN)

    def to_s3_resource_url(self) -> str:
        return  (self.folder + '/' if self.folder != None else '') + \
                self.to_simple_file_name()


class S3Artifact(Artifact):

    def __init__(self, name:str, type:str = None, version:str = None):
        super().__init__(name, 'AWS-S3-{}'.format(type))
        self.ext = type
        self.version = version

    def get_simple_name(self):
        return self.name + ('-' + self.version if self.version != None else '') + '.' + (self.ext if self.ext != None else UNKNOWN)

    def get_full_name(self):
        return self.name + '/' + self.get_simple_name()

    def is_latest_version(self) -> bool:
        return self.version == None or self.version == LATEST_VERSION

    def get_metadata(self) -> S3ArtifactMetadata:
        return S3ArtifactMetadata(self.name, self.name, self.version, self.ext)


class JmeterArtifact(S3Artifact):

    def __init__(self, version: str = None):
        super().__init__('jmeter', 'zip', version)

class DummyArtifact(S3Artifact):

    def __init__(self, version: str = None):
        super().__init__('dummy', 'txt', version)

class ArtifactsManager:

    __artifacts_repository_bucket__ = 'runfalcon-repository'
    __logger:Logger = Logger('ArtifactsManager')

    def __init__(self):
        pass

    def __get_download_from_s3_script(self, artifact_s3_full_url:str, output_folder:str) -> str:
        script:str = '#!/bin/bash\n'
        script += 'set -e\n'
        script += 'aws s3 cp {artifact_url} {output_folder}\n' \
                    .format( \
                        artifact_url = artifact_s3_full_url, \
                        output_folder = output_folder)
        return script

    def __get_s3_artifact_url(self, metadata:S3ArtifactMetadata) -> str:
        artifact_url:str = 's3://{bucket}/{artifact}' \
                                .format( \
                                    bucket = self.__artifacts_repository_bucket__, \
                                    artifact = metadata.to_s3_resource_url())
        return artifact_url

    def __get_artifact_metadata__(self, artifact:S3Artifact) -> S3ArtifactMetadata:
        metadata:S3ArtifactMetadata = S3ArtifactMetadata(artifact.name, 'metadata', None, 'txt')

        self.__logger.info('Downloading metadata for {} ...'.format(metadata.to_s3_resource_url()))

        output_folder:str =  get_runfalcon_tmp_dir()
        script:str = self.__get_download_from_s3_script(self.__get_s3_artifact_url(metadata), output_folder)
        executor:CommandLineExecutor = CommandLineExecutor()
        executor.execute_script(script)

        props:Properties = Properties()
        props.load(output_folder + '/' + metadata.to_simple_file_name())
        latest_version:str = props.get('latest-version')
        
        artifact_metadata:S3ArtifactMetadata = artifact.get_metadata()
        
        if artifact.is_latest_version():
            artifact_metadata.latest_version = latest_version

        artifact_metadata.type = props.get('artifact-type')

        return artifact_metadata


    def __download_artiact_from_aws_s3(self, artifact:S3Artifact) -> str:
        metadata:S3ArtifactMetadata = self.__get_artifact_metadata__(artifact)
        output_folder:str = get_runfalcon_tmp_dir()
        s3_url:str = self.__get_s3_artifact_url(metadata)
        script:str = self.__get_download_from_s3_script(s3_url, output_folder)

        executor:CommandLineExecutor = CommandLineExecutor()
        self.__logger.info('Downloading {artifact} ...'.format(artifact = s3_url))
        executor.execute_script(script)
        return output_folder + '/' + metadata.to_simple_file_name()

    def get_artifact(self, artifact:Artifact) -> str:
        if isinstance(artifact, S3Artifact):
            return self.__download_artiact_from_aws_s3(artifact)
        return None
