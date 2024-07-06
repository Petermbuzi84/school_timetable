import json


class Subject:
    @property
    def load(self) -> list[dict]:
        """
        load the subjects from file
        :return: all the subjects
        """
        filepath: str = "storage/subjects.json"
        with open(filepath, "r") as f:
            subs: list[dict] = json.load(f)
        return subs
