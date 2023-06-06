import yaml


class RedmineConfig:
    _instance = None

    @staticmethod
    def get_instance():
        if RedmineConfig._instance is None:
            RedmineConfig._instance = RedmineConfig()
        return RedmineConfig._instance

    def _check_singleton(self):
        if RedmineConfig._instance is None or self != RedmineConfig._instance:
            raise Exception("This class is a singleton, you must get this using get_instance()!")

    def load(self, config_file):
        self._check_singleton()
        with open(config_file, 'r') as f:
            self.data = yaml.safe_load(f)

    def get_status_string(self, status_code):
        self._check_singleton()
        return self.data['STATUS_CODE_TO_STRING'].get(str(status_code), "UNKNOWN")

    def get_redmine_url(self):
        self._check_singleton()
        return self.data['REDMINE']['url']

    def get_redmine_key(self):
        self._check_singleton()
        return self.data['REDMINE']['key']

    def get_redmine_query_ratio(self):
        self._check_singleton()
        return self.data['REDMINE']['query_ratio']
