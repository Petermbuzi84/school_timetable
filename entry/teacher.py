import json


class Teacher:
    def __init__(self, subjects: list[dict]):
        self.__subjects: list[dict] = subjects

    def __link_subject_teacher(self, in_teachers: list[dict]) -> None:
        """
        # loop though the teachers
        # loop (nested) through the subjects
        # loop (nested) through the teachers subjects
        # match the teacher to the subject and add the details from the subject
        # these details include: name, (code), category and workload
        # make sure to remove the forms attribute and instead modify the workload to only include
         the teacher's subjects
        :param in_teachers: loaded list of teachers
        :return: updated list of teachers
        """
        subjects: list[dict] = self.__subjects
        for teacher in in_teachers:
            for i in range(len(teacher["subjects"])):
                teacher_subject: dict = teacher["subjects"][i]
                for subject in subjects:
                    if subject["code"] == teacher_subject["code"]:
                        workload: dict = {}
                        for form in teacher_subject["forms"]:
                            workload[form] = subject["workload"][form]
                        teacher_subject["workload"] = workload
                        teacher_subject["name"] = subject["name"]
                        teacher_subject["category"] = subject["category"]
                        break

    @property
    def load(self) -> list[dict]:
        """
        load the teachers from file then pass it to the link subject teacher
        method
        :return: updated list of teachers
        """
        filepath: str = "storage/teachers.json"
        with open(filepath, "r") as f:
            teach: list[dict] = json.load(f)
        self.__link_subject_teacher(teach)
        return teach

    @staticmethod
    def subjects(teachers: list[dict], teacher_id: int) -> list[dict]:
        """
        gets all the subjects for a selected teacher
        :param teachers: list of all the teachers
        :param teacher_id: the id of a selected teacher
        :return: list of subjects for teacher
        """
        teacher_subjects: list[dict] = []
        for teacher in teachers:
            if teacher["id"] == teacher_id:
                teacher_subjects = teacher["subjects"]
                break
        return teacher_subjects
