import logging

from models.stepik import (
    CoursesResponse,
    Lesson,
    LessonResponse,
    Section,
    SectionsResponse,
    Step,
    StepResponse,
    SubmissionResponse,
    UnitsResponse,
)
from oauth import API_URL, get_session

logger = logging.getLogger(__name__)


class StepikClient:
    def __init__(self):
        self.session = get_session()

    def _get(self, url) -> dict:
        resp = self.session.get(url)
        resp.raise_for_status()
        return resp.json()

    def get_section_id(self, course_id: int, section_no: int) -> int:
        course_json = self._get(f"{API_URL}/courses/{course_id}")
        course_resp = CoursesResponse.model_validate(course_json)
        sections_ids = course_resp.courses[0].sections
        if not (0 < section_no <= len(sections_ids)):
            raise IndexError("Секции с таким номером не существует")
        return sections_ids[section_no - 1]

    def get_section(self, id: int) -> Section:
        section_json = self._get(f"{API_URL}/sections/{id}")
        section_resp = SectionsResponse.model_validate(section_json)
        return section_resp.sections[0]

    def get_lesson(self, id: int) -> Lesson:
        lesson_json = self._get(f"{API_URL}/lessons/{id}")
        lesson_resp = LessonResponse.model_validate(lesson_json)
        return lesson_resp.lessons[0]

    def get_lessons(self, course_id: int, section_no: int) -> list[Lesson]:
        section = self.get_section(self.get_section_id(course_id, section_no))
        lessons = []
        for unit_id in section.units:
            unit_json = self._get(f"{API_URL}/units/{unit_id}")
            unit_resp = UnitsResponse.model_validate(unit_json)
            lessons.append(self.get_lesson(unit_resp.units[0].lesson))
        return lessons

    def get_step(self, id: int) -> Step:
        step_json = self._get(f"{API_URL}/steps/{id}")
        step_resp = StepResponse.model_validate(step_json)
        return step_resp.steps[0]

    def get_solution_code(self, step_id: int) -> str | None:
        submission_json = self._get(f"{API_URL}/submissions?step={step_id}")
        submission_resp = SubmissionResponse.model_validate(submission_json)
        for submission in reversed(submission_resp.submissions):
            if submission.status == "correct":
                return submission.reply.code
        return None
