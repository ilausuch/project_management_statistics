import os
import yaml


class ConfigParser:
    def __init__(self, parser):
        self.parser = parser
        parser.add_argument('--config', type=str, help='Configuration file')

    def parse_args(self):
        args = vars(self.parser.parse_args())
        config_file = args.get('config')

        if config_file and os.path.exists(config_file):
            with open(config_file, mode="r", encoding="utf-8") as ymlfile:
                config = yaml.safe_load(ymlfile)

            if not isinstance(config, dict):
                raise ValueError("Config file must be a yaml with key: values pairs")

            for key, value in config.items():
                if key not in args or args[key] is None:
                    args[key] = value
        return args
