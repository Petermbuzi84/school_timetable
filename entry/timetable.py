import json
from random import randint
from entry.teacher import Teacher
from entry.lesson import Lesson
from entry.subject import Subject


class Timetable:
    def __init__(self, forms: list[dict]):
        subject: Subject = Subject()
        self.__subjects: list[dict] = subject.load
        self.__teacher: Teacher = Teacher(self.__subjects)
        self.__lesson: Lesson = Lesson(forms)
        self.__teachers: list[dict] = self.__teacher.load
        self.__days: list[str] = ["mon", "tue", "wed", "thur", "fri"]
        self.__max_days: int = len(self.__days) - 1  # randint includes the end value
        self.__max_lessons: int = 8  # the lessons have a length of 9, but randint includes the last value
        self.__rejected_days: list[str] = []
        self.__doubles_filled: list[dict] = []
        self.__filled: dict = {
            "mon": [],  # {index: 0, subject: [102]}
            "tue": [],  # {index: 5, subject: [232, 233]}
            "wed": [],
            "thur": [],
            "fri": []
        }

    @property
    def __available_days(self) -> list[int]:
        my_days: list[int] = []
        for i in range(len(self.__days)):
            day: str = self.__days[i]
            if len(self.__filled[day]) < 9:
                my_days.append(i)
        return my_days

    def __filled_days(self, subject: dict) -> list[int]:
        my_days: list[int] = []
        for i in range(len(self.__days)):
            day: str = self.__days[i]
            if len(self.__filled[day]) == 9:
                found: bool = False
                for slot in self.__filled[day]:
                    if slot["subject"][0]["code"] == subject["code"]:
                        found = True
                        break
                if not found:
                    my_days.append(i)
        return my_days

    def __subject_filled_days(self, subject: dict) -> list[str]:
        fill_days: list[str] = []
        for day in self.__days:
            for fill in self.__filled[day]:
                if fill["subject"]["code"] == subject["code"]:
                    fill_days.append(day)
        return fill_days

    def __subject_unfilled_days(self, subject: dict) -> list[str]:
        un_fill_days: list[str] = []
        for day in self.__days:
            found: bool = False
            for fill in self.__filled[day]:
                if fill["subject"][0]["code"] == subject["code"]:
                    found = True
                    break
            if not found:
                un_fill_days.append(day)
        return un_fill_days

    @property
    def __selected_day_from_whole_week(self) -> str:
        start: int = 0
        day_index: int = randint(start, self.__max_days)
        return self.__days[day_index]

    def __selected_day(self, avail_days: list[int]) -> str:
        start: int = 0
        day_index: int = randint(start, len(avail_days) - 1)
        return self.__days[avail_days[day_index]]

    def __fill_empty_slots(self, forms: dict, form: str) -> None:
        lessons: list = forms[form]
        self.__lesson.empty_slots = []
        self.__lesson.index_empty_slots(lessons)

    def __selected_lesson(self) -> int:
        start: int = 0
        index: int = randint(start, len(self.__lesson.empty_slots) - 1)
        return self.__lesson.empty_slots[index]

    @property
    def __load(self) -> dict:
        filepath: str = "storage/template.json"
        with open(filepath, "r") as f:
            timetable: dict = json.load(f)
        return timetable

    def __select_filled_lesson(self, day: str) -> tuple[dict, int]:
        start: int = 0
        index: int = randint(start, len(self.__filled[day]) - 1)
        return self.__filled[day][index], index

    @staticmethod
    def __select_filled_lesson_from_given(max_index: int) -> int:
        start: int = 0
        return randint(start, max_index)

    def __double_day_filled(self, day: str) -> bool:
        day_filled: bool = False
        for double in self.__doubles_filled:
            if double["day"] == day:
                day_filled = True
                break
        return day_filled

    def __un_doubled_subjects(self, day: str) -> list[dict]:
        subjects: list[dict] = []
        for fill in self.__filled[day]:
            found: bool = False
            if fill["subject"][0]["category"] == "science":
                for double in self.__doubles_filled:
                    if fill["subject"][0]["code"] == double["subject"]["code"]:
                        found = True
                        break
            if not found:
                subjects.append(fill)
        return subjects

    def __subject_with_less_than_five_workload(self, day: str, form: str) -> list[dict]:
        subjects: list[dict] = []
        filled_un_doubles: list[dict] = self.__un_doubled_subjects(day)
        for fill in filled_un_doubles:
            for subject in self.__lesson.subjects:
                if fill["subject"][0]["code"] == subject["code"] and subject["workload"][form]["work"] < 5:
                    subjects.append(fill)
                    break
        return subjects

    def __two_subjects_with_less_than_five_workload(self, day: str, form: str) -> list[dict]:
        subjects: list[dict] = []
        index: int = -10
        if not self.__double_day_filled(day):
            for i in range(len(self.__filled[day])):
                fill: dict = self.__filled[day][i]
                found: bool = False
                for subject in self.__lesson.subjects:
                    if fill["subject"][0]["code"] == subject["code"]:
                        if subject["workload"][form]["work"] < 5:
                            if abs(index - fill["index"]) == 1:
                                subjects = [self.__filled[day][i], self.__filled[day][i-1]]
                                found = True
                            index = fill["index"]
                        break
                if found:
                    break
        return subjects

    def __switch_for_double_subject(self, conflict_subject: dict, form: str) -> None:
        for day in self.__days:
            five_less_subjects: list[dict] = self.__two_subjects_with_less_than_five_workload(day, form)

    def __days_with_single_empty_slots(self, days: list[str], timetable: dict) -> list[str]:
        days_with_slot: list[str] = []
        for day in days:
            if self.__lesson.is_empty_slots(timetable[day]):
                days_with_slot.append(day)
        return days_with_slot

    def __switch_for_single_subject(self, conflict_subject: dict, timetable: dict, form: str) -> None:
        days_without_subject: list[str] = self.__subject_unfilled_days(conflict_subject)
        for day in days_without_subject:
            five_less_subjects: list[dict] = self.__subject_with_less_than_five_workload(day, form)
            for five_less_subject in five_less_subjects:
                days_without_five_less_subject: list[str] = self.__subject_unfilled_days(five_less_subject)
                days_with_slot: list[str] = self.__days_with_single_empty_slots(
                    days_without_five_less_subject, timetable
                )

    def __switch_with_another_subject(self, conflict_subject: dict, timetable: dict, form: str) -> None:
        if conflict_subject["category"] == "science" and not self.__science_double_filled(conflict_subject):
            self.__switch_for_double_subject(conflict_subject, form)
        else:
            self.__switch_for_single_subject(conflict_subject, timetable, form)

    def __validate_day_available_for_subject(self, subject: dict, timetable: dict, form: str) -> str:
        avail_days: list[int] = self.__available_days
        fill_days: list[int] = self.__filled_days(subject)
        visited: list[str] = []
        while True:
            if len(visited) == len(avail_days):
                self.__switch_with_another_subject(subject, timetable, form)
                avail_days = self.__available_days
                fill_days = self.__filled_days(subject)
                visited = []
            day: str = self.__selected_day(avail_days)
            if day in visited:
                continue
            else:
                visited.append(day)
            if subject["category"] == "science" and not self.__science_double_filled(subject) \
                    and not self.__lesson.double_slot_available(timetable[day][form]):
                continue
            if len(self.__filled[day]) != self.__max_lessons + 1:
                found: bool = False
                for filled in self.__filled[day]:
                    if filled["subject"][0]["code"] == subject["code"]:
                        found = True
                        break
                if not found or self.__lesson.workload_greater_than_five(subject, form):
                    rejected: bool = False
                    for reject in self.__rejected_days:
                        if reject == day:
                            rejected = True
                            break
                    if not rejected:
                        break
        return day

    def __science_double_day(self, subject: dict) -> str:
        if subject["category"] == "science":
            found: bool = False
            index: int = 0
            while index < len(self.__doubles_filled):
                double: dict = self.__doubles_filled[index]
                if double["subject"] == subject["code"]:
                    found = True
                    break
                index += 1
            if found:
                return self.__doubles_filled[index]["day"]
        return ""

    def __science_double_filled(self, subject: dict) -> bool:
        if subject["category"] == "science":
            found: bool = False
            for double in self.__doubles_filled:
                if double["subject"]["code"] == subject["code"]:
                    found = True
                    break
            if not found:
                return False
        return True

    @staticmethod
    def __validate_science_double(my_lesson: int) -> int:
        if my_lesson % 2 == 0 and my_lesson != 8:
            return my_lesson + 1
        return my_lesson - 1

    def __validate_conflicts(self, my_lesson: int, day: str, forms: dict, form: str, update: bool) -> bool:
        if self.__lesson.lesson_filled(my_lesson, day, self.__filled):
            update = True
        elif self.__lesson.teacher_conflicting(forms, form, my_lesson):
            update = True
        return update

    def __validate_lesson_filled_or_change_day(
            self, forms: dict, form: str, day: str, subject: dict) -> tuple[bool, int, int]:
        change: bool = False
        update: bool = True
        my_lesson: int = -1
        double_lesson: int = -1
        self.__fill_empty_slots(forms, form)
        while update:
            change = self.__lesson.timetable_day_unavailable(my_lesson)
            update = False
            if change:
                self.__rejected_days.append(day)
                break
            my_lesson = self.__selected_lesson()
            update = self.__validate_conflicts(my_lesson, day, forms, form, update)
            if not update and not self.__science_double_filled(subject):
                double_lesson = self.__validate_science_double(my_lesson)
                update = self.__validate_conflicts(double_lesson, day, forms, form, update)
        return change, my_lesson, double_lesson

    def __lesson_fill_or_change_day(self, forms: dict, form: str, day: str, subject: dict) -> bool:
        lessons: list = forms[form]
        change, lesson_index, double_lesson_index = self.__validate_lesson_filled_or_change_day(
            forms, form, day, subject
        )
        if change:
            return True
        lessons[lesson_index] = subject
        subject["workload"][form]["work"] -= 1
        self.__filled[day].append({"index": lesson_index, "subject": [subject]})
        if double_lesson_index > -1:
            lessons[double_lesson_index] = subject
            subject["workload"][form]["work"] -= 1
            self.__filled[day].append({"index": double_lesson_index, "subject": [subject]})
            self.__doubles_filled.append({"day": day, "subject": subject})
        self.__filled[day].sort(key=lambda value: value["index"])
        return False

    def __set_lesson(self, subject: dict, timetable: dict, form: str) -> None:
        day: str = self.__validate_day_available_for_subject(subject, timetable, form)
        forms: dict = timetable[day]
        change: bool = self.__lesson_fill_or_change_day(forms, form, day, subject)
        if change:
            self.__set_lesson(subject, timetable, form)

    def fill(self, form: str) -> None:
        timetable: dict = self.__load
        for teach in self.__teachers:
            teacher_id: int = teach["id"]
            subjects: list[dict] = self.__teacher.subjects(self.__teachers, teacher_id)
            for subject in subjects:
                while form in subject["workload"] and subject["workload"][form]["work"] > 0:
                    if subject["code"] == 233:
                        print()
                    self.__set_lesson(subject, timetable, form)
        print(timetable)
