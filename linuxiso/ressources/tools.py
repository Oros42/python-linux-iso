import logging
import subprocess
import os
import json
import yaml
from jsonschema import validate


def load_conf(confFile=None, confJson=None, confDict=None):
    """
    Load & check configuration
    :return : configuration valided
    """
    dir_path = os.path.dirname(os.path.realpath(__file__))
    conf_schema = os.path.join(
        dir_path,
        '..',
        'ressources',
        'conf_jsonschema.json')

    # # Get inital conf
    # confDefaultFile = os.path.join(dir_path, '..', 'conf', 'settings.yaml')
    # with open(confDefaultFile, "r") as f:
    #     conf1 = yaml.load(f)

    if confFile:
        with open(confFile, "r") as f:
            conf2 = yaml.load(f)
    elif confJson:
        conf2 = json.loads(confJson)
    else:
        conf2 = confDict

    conf = conf2
    assert conf, 'No configuration given'

    # print(json.dumps(conf, indent=4))
    with open(conf_schema, "r") as f:
        dict_schema = json.load(f)

    # If no exception, the conf is valided
    validate(conf, dict_schema)
    return conf


def run_cmd(cmd):
    """
    Run a command
    if error, print and raise it
    params cmd : String commande
    return out
    """
    logging.debug('Run command "'+cmd+'"')
    try:
        process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        process.check_returncode()

    except Exception as e:
        logging.exception(str(e) +"\nCMD_SHELL : "+cmd+"\nSTDOUT : "+process.stdout.decode()+"\nSTDERR : "+process.stderr.decode(), exc_info=True)
        #logging.critical("{CDM : "+cmd+", "} : "+cmd)
        #logging.critical("STDOUT : "+process.stdout.decode())
        #logging.critical("STDERR : "+process.stderr.decode())
        #raise e

    return process.stdout.decode()


def setup_logging(
    default_path='logging.yaml',
    default_level=logging.INFO,
    env_key='LOG_CFG'
):
    """
    Setup logging configuration
    """
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)
