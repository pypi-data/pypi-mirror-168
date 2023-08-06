from typing import List


class NotDataclassError(Exception):
    pass


class NoSuchFieldsError(Exception):
    def __init__(self, fields: List[str]):
        super().__init__("Expected fields missing in config class" + " ".join(fields))
