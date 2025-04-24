from models.stepik import Lesson, LessonResponse, Step, StepResponse, SubmissionResponse
from oauth import API_URL, session


class StepikClient:
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
