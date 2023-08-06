import json
from runfalconbuildtools.command_line_executor import CommandLineExecutor

class AWSCommandParams:
    zone:str
    account:int

    def __init__(self, account:int = None, zone:str = None):
        self.account = account
        self.zone = zone

class AWSClient:

    def __init__(self, params:AWSCommandParams = AWSCommandParams()):
        self.params = params

    def get_ecr_image_data(self, repository:str, image_tag:str):
        executor:CommandLineExecutor = CommandLineExecutor()
        command:str = ''
        command += '#!/bin/sh\n'
        command += 'set -e\n'
        command += 'aws ecr list-images --repository-name {repository}\n'.format(repository = repository)

        try:
            executor.execute_script(command)
        except:
            return None

        json_data = json.loads(executor.stdout)
        for img in json_data["imageIds"]:
            if img["imageTag"] == image_tag:
                return img

        return None

    def delete_image_from_ecr(self, repository:str, image_digest:str):
        executor:CommandLineExecutor = CommandLineExecutor()
        command:str = ''
        command += '#!/bin/sh\n'
        command += 'set -e\n'
        command += 'aws ecr batch-delete-image --repository-name {repository} --image-ids imageDigest={image_digest}\n' \
                    .format(repository = repository, image_digest = image_digest)

        executor.execute_script(command)
        if executor.return_code != 0:
            raise Exception('\nCode: {code}.\noutput: {out}\nerror: {error}' \
                .format(code = executor.return_code, out = executor.stdout, error = executor.stderr))

    def push_image_to_ecr(self, source_image:str, repository:str, delete:bool = True):
        target_image:str = source_image.replace(':', '-')

        if delete:
            image_data = self.get_ecr_image_data(repository, target_image)
            if image_data != None:
                self.delete_image_from_ecr(repository, image_data["imageDigest"])

        executor:CommandLineExecutor = CommandLineExecutor()
        command:str = ''
        command += '#!/bin/sh\n'
        command += 'set -e\n'
        command += 'echo "Login in to docker ..."\n'
        command += 'aws ecr get-login-password --region {zone} | docker login --username AWS --password-stdin {account}.dkr.ecr.{zone}.amazonaws.com\n' \
                        .format(zone = self.params.zone, account = self.params.account)
        command += 'echo "Tagging image ..."\n'
        command += 'docker tag {source_image} {account}.dkr.ecr.{zone}.amazonaws.com/{repository}:{target_image}\n' \
                        .format(source_image = source_image, account = self.params.account, zone = self.params.zone, repository = repository, target_image = target_image)
        command += 'echo "Pushig image ..."\n'
        command += 'docker push {account}.dkr.ecr.{zone}.amazonaws.com/{repository}:{target_image}\n' \
                        .format(account = self.params.account, zone = self.params.zone, repository = repository, target_image = target_image)

        executor.execute_script(command)
        if executor.return_code != 0:
            raise Exception('\nCode: {code}.\noutput: {out}\nerror: {error}' \
                .format(code = executor.return_code, out = executor.stdout, error = executor.stderr))

    def get_from_s3(self, artifact_s3_full_url:str, outdir:str = '.', recursive:bool = False):
        command:str = '#!/bin/sh\n'
        command += 'set -e\n'
        command += 'aws s3 cp {artifact_url} {outdir} {recursive}\n' \
                    .format( \
                        artifact_url = artifact_s3_full_url, \
                        outdir = outdir, \
                        recursive = ('--recursive' if recursive else ''))

        executor:CommandLineExecutor = CommandLineExecutor()
        executor.execute_script(command)
        if executor.return_code != 0:
            raise Exception('\nCode: {code}.\noutput: {out}\nerror: {error}' \
                .format(code = executor.return_code, out = executor.stdout, error = executor.stderr))
