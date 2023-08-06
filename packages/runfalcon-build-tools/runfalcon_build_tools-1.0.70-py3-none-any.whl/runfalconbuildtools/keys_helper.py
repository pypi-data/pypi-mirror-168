from runfalconbuildtools.aws_client import AWSClient

class KeysHelper:

    __artifacts_keys_bucket__ = 'runfalcon-repository'

    def __init__(self, application:str, env:str):
        self.application = application
        self.env = env

    def __get_s3_url__(self) -> str:
        url:str = 's3://runfalcon-repository/{app}-ssh-keys/{env}'.format(app = self.application, env =self.env)
        return url

    def get_ssh_keys(self, outdir:str = '.'):
        aws_client:AWSClient = AWSClient()
        aws_client.get_from_s3(self.__get_s3_url__(), outdir, True)

