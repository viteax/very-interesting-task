from pydantic import BaseModel


class Lesson(BaseModel):
    id: int
    steps: list[int]


class LessonResponse(BaseModel):
    meta: dict
    lessons: list[Lesson]


class Block(BaseModel):
    name: str
    text: str


class Step(BaseModel):
    id: int
    block: Block


class StepResponse(BaseModel):
    meta: dict
    steps: list[Step]


class CodeProblem(BaseModel):
    title: str
    description: list[str]


class Reply(BaseModel):
    code: str
    language: str


class Submission(BaseModel):
    id: int
    status: str
    reply: Reply


class SubmissionResponse(BaseModel):
    meta: dict
    submissions: list[Submission]


class CodeSolution(BaseModel):
    title: str
    description: list[str]
    pic_path: str
