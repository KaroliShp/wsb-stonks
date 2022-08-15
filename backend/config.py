import os
import configparser
import enum

# TODO: move to a shared enum types file
class DeploymentEnv(enum.Enum):
    Dev = 1
    Prod = 2

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'


    def __init__(self, environment, secrets_file = "./secrets"):
        config_parser = configparser.ConfigParser()
        config_parser.optionxform = str
        config_parser.read(secrets_file)

        self.config = dict(config_parser.items("MANDATORY"))
        
        if environment == "dev":
            self.env = DeploymentEnv.Dev
            self.config.update(dict(config_parser.items("DEV")))
        elif environment == "prod":
            self.env = DeploymentEnv.Prod
            self.config.update(dict(config_parser.items("PROD")))