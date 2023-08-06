import os
import enum
import json


from rhdzmota.settings import logger_manager


logger = logger_manager.get_logger(name=__name__)


class Country(enum.Enum):
    MEXICO = "MX"

    @property
    def subdivisions_data_filepath(self) -> str:
        filename = f"{self.value}.json".lower()
        filepath = os.path.join(os.path.dirname(__file__), "datafiles", filename)
        if os.path.exists(filepath):
            return filepath
        logger.error("Missing datafile for %s", self.name)
        return os.path.join(os.path.dirname(filepath), "default.json")

    @property
    def subdivisions(self):
        data_filepath = self.subdivisions_data_filepath
        with open(data_filepath, "r") as file:
            payload = json.loads(file.read())
        return enum.Enum(self.name, payload)
