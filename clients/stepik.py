import logging

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
from oauth import API_URL, get_session

logger = logging.getLogger(__name__)


class StepikClient:
    session = get_session()

    def get_section_id(self, course_id: int, section_no: int) -> int:
        resp = self.session.get(f"{API_URL}/courses/{course_id}")
        course_resp = CoursesResponse.model_validate(resp.json())
        sections_ids = course_resp.courses[0].sections
        if not (0 < section_no <= len(sections_ids)):
            raise IndexError("Секции с таким номером не существует")
        return sections_ids[section_no - 1]

    def get_section(self, id: int):
        resp = self.session.get(f"{API_URL}/sections/{id}")
        section_resp = SectionsResponse.model_validate(resp.json())
        return section_resp.sections[0]

    def get_lesson(self, id: int) -> Lesson:
        resp = self.session.get(f"{API_URL}/lessons/{id}")
        lesson_resp = LessonResponse.model_validate(resp.json())
        return Lesson.model_validate(lesson_resp.lessons[0])

    def get_lessons(self, course_id: int, section_no: int) -> list[Lesson]:
        section = self.get_section(self.get_section_id(course_id, section_no))
        lessons = []
        for unit_id in section.units:
            resp = self.session.get(f"{API_URL}/units/{unit_id}")
            unit_resp = UnitsResponse.model_validate(resp.json())
            lessons.append(self.get_lesson(unit_resp.units[0].lesson))
        return lessons

    def get_step(self, id: int) -> Step:
        resp = self.session.get(f"{API_URL}/steps/{id}")
        step_resp = StepResponse.model_validate(resp.json())
        return step_resp.steps[0]

    def get_solution_code(self, step_id: int) -> str | None:
        resp = self.session.get(f"{API_URL}/submissions?step={step_id}")
        submission_resp = SubmissionResponse.model_validate(resp.json())
        for submission in reversed(submission_resp.submissions):
            if submission.status == "correct":
                return submission.reply.code
        return None
