from models.stepik import (
    CoursesResponse,
    Lesson,
    LessonResponse,
    SectionsResponse,
    Step,
    StepResponse,
    SubmissionResponse,
    UnitsResponse,
)
from oauth import API_URL, session


class StepikClient:
    def get_lessons_ids(self, course_id: int, section_no: int) -> list[int]:
        resp = session.get(f"{API_URL}/courses/{course_id}")
        course_resp = CoursesResponse.model_validate(resp.json())
        sections_ids = course_resp.courses[0].sections
        if not (0 < section_no <= len(sections_ids)):
            raise IndexError("Секции с таким номером не существует")

        section_id = sections_ids[section_no - 1]
        resp = session.get(f"{API_URL}/sections/{section_id}")
        section_resp = SectionsResponse.model_validate(resp.json())
        section = section_resp.sections[0]

        lessons_ids = []
        for unit_id in section.units:
            resp = session.get(f"{API_URL}/units/{unit_id}")
            unit_resp = UnitsResponse.model_validate(resp.json())
            lessons_ids.append(unit_resp.units[0].lesson)
        return lessons_ids

    def get_lesson(self, id: int) -> Lesson:
        resp = session.get(f"{API_URL}/lessons/{id}")
        lesson_resp = LessonResponse.model_validate(resp.json())
        return Lesson.model_validate(lesson_resp.lessons[0])

    def get_step(self, id: int) -> Step:
        resp = session.get(f"{API_URL}/steps/{id}")
        step_resp = StepResponse.model_validate(resp.json())
        return step_resp.steps[0]

    def get_solution_code(self, step_id: int) -> str:
        resp = session.get(f"{API_URL}/submissions?step={step_id}")
        submission_resp = SubmissionResponse.model_validate(resp.json())
        for submission in reversed(submission_resp.submissions):
            if submission.status == "correct":
                return submission.reply.code
        return "Error, no correct ones"
