import yaml

DEBUGGING_LEVEL_1 = False
DEBUGGING_LEVEL_2 = False
PRINT_OBJECT = False
# add the absolute path for opening of config.yaml file 
with open("config.yaml", "r") as strm:
    config = yaml.safe_load(strm)

    URL = config['url_v21']
    USERNAME = config['username']
    PASSWORD = config['password']
    COLLECTION = config['collections']
    PATH = config['path']
    VERSION = config['version']
