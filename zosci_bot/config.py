import yaml

from schema import Schema, Optional


def get_schema():
    config_schema = Schema(
        {Optional('config'): {
            Optional('plugins', default=[]): list,
        },
         'mattermost': {
            'url': str,
            'port': lambda p: 1 <= p < 65535,
            Optional('api_path', default='/api/v4'): str,
            'token': str,
            'team': str,
            Optional('ssl_verify', default=True): bool,
        },
         # this allows to keep the 'clouds' section used by the openstacksdk.
         Optional('clouds'): object,
         Optional('prometheus'): {
             'url': str,
             Optional('ssl_verify', default=False): bool,
         }
    })
    return config_schema


def load_config(fpath):
    with open(fpath) as f:
        configuration = yaml.safe_load(f)
        config_schema = get_schema()
        return config_schema.validate(configuration)
