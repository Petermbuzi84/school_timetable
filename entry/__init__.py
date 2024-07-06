from entry.timetable import Timetable


class Entry:
    def __init__(self):
        self.__forms: list[dict] = [
            {"form": "f1", "combined": False},
            {"form": "f2", "combined": True},
            {"form": "f3", "combined": True},
            {"form": "f4", "combined": True}
        ]
        self.__timetable: Timetable = Timetable(self.__forms)

    def run(self) -> None:
        form: dict = self.__forms[0]
        self.__timetable.fill(form["form"])
