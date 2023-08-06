from argparse import ArgumentParser
from pathlib import Path
from pydoc import importfile

from .config import Config


JSON_NAME = "assertio.json"
YAML_NAME = "assertio.yaml"


class _CLI:
    def __init__(self):
        flags = ArgumentParser()
        flags.add_argument(
            "--run",
            default="all",
        )
        flags.add_argument(
            "--settings",
            "-s",
            default=None
        )
        self._flags, _ = flags.parse_known_args()

    def load_modules(self):
        modules = []
        for p in Path.cwd().joinpath("features/runners").glob("**/*.py"):
            modules.append(importfile(str(p)))
        return modules
    
    def get_runners_for(self, module):
        return [
            getattr(module, name) 
            for name in dir(module) 
            if name.endswith("Runner") and name != "Runner"
        ]

    def run_all(self):
        for module in self.load_modules():
            for runner in self.get_runners_for(module):
                runner().start()
    
    def run_one(self):
        for module in self.load_modules():
            for runner in self.get_runners_for(module):
                if self._flags.run == runner.__name__:
                    runner().start()

    def get_config(self) -> Config:
        _ = Config()
        if self._flags.settings is None:
            _.from_json(JSON_NAME)
            _.from_yaml(YAML_NAME)
        elif self._flags.settings.endswith("json"):
            _.from_json(self._flags.settings)
        elif self._flags.settings.endswith("yaml"):
            _.from_yaml(self._flags.settings)
        
        return _


    def bootstrap(self):
        if self._flags.run == "all":
            self.run_all()
        else:
            self.run_one()
