from entry.subject import Subject


class Lesson:
    def __init__(self, forms: list[dict]):
        self.__forms: list[dict] = forms
        subject: Subject = Subject()
        self.subjects: list[dict] = subject.load
        self.empty_slots: list[int] = []

    def index_empty_slots(self, lessons: list) -> None:
        for i in range(len(lessons)):
            lesson = lessons[i]
            if lesson == "":
                self.empty_slots.append(i)

    @staticmethod
    def is_empty_slots(lessons: list) -> bool:
        for lesson in lessons:
            if lesson == "":
                return True
        return False

    @staticmethod
    def lesson_filled(index: int, day: str, filled: dict) -> bool:
        """
        # check if the subject is filled in the lesson index
        :param index: selected lesson index
        :param day: selected day
        :param filled: filled subjects and their positions
        :return: selected or updated lesson index
        """
        found: bool = False
        for lesson in filled[day]:
            if lesson["index"] == index:
                found = True
                break
        return found

    def teacher_conflicting(self, forms: dict, in_form: str, index: int) -> bool:
        """
        # check if the subjects above and below are of the same teacher in the current
        # position
        :param forms: list of all the lessons for all the classes
        :param in_form: currently selected form
        :param index: selected lesson
        :return: conflicting status
        """
        conflict: bool = False
        for form in self.__forms:
            if form["form"] != in_form:
                lessons: list[dict] = forms[in_form]
                if lessons[index] != "" and lessons[index]["teacher"] == forms[form["form"]][index]["teacher"]:
                    conflict = True
                    break
        return conflict

    def timetable_day_unavailable(self, index: int) -> bool:
        """
        there will be cases where none of the empty slots fit
        the selected subject, a need therefore arises to change
        the day
        :param index:
        :return:
        """
        for i in range(len(self.empty_slots)):
            slot: int = self.empty_slots[i]
            if slot == index:
                prev_index: int = len(self.empty_slots)
                self.empty_slots.pop(i)
                if prev_index > 1:
                    return False
        return len(self.empty_slots) == 0

    def workload_greater_than_five(self, in_subject: dict, form: str) -> bool:
        """
        loops through the unmodified subjects which contains the
        original workload
        :param in_subject: modified selected subject
        :param form: selected form
        :return: status of either greater than five or not
        """
        for subject in self.subjects:
            if subject["code"] == in_subject["code"]:
                if subject["workload"][form]["work"] > 5:
                    return True
                break
        return False

    def workload_equal_to_five(self, in_subject: dict, form: str) -> bool:
        """
        loops through the unmodified subjects which contains the
        original workload
        :param in_subject: modified selected subject
        :param form: selected form
        :return: status of either equal to five or not
        """
        for subject in self.subjects:
            if subject["code"] == in_subject["code"]:
                if subject["workload"][form]["work"] == 5:
                    return True
                break
        return False

    @staticmethod
    def double_slot_available(lessons: list) -> bool:
        last_index: int = -10
        for i in range(len(lessons)):
            lesson = lessons[i]
            if lesson == "":
                if last_index == i - 1:
                    return True
                last_index = i
        return False
