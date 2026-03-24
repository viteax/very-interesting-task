from pydantic import BaseModel, ConfigDict


class _BaseResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")


class Course(BaseModel):
    id: int
    sections: list[int]


class CoursesResponse(_BaseResponse):
    courses: list[Course]


class Section(BaseModel):
    id: int
    units: list[int]
    title: str


class SectionsResponse(_BaseResponse):
    sections: list[Section]


class Unit(BaseModel):
    id: int
    lesson: int


class UnitsResponse(_BaseResponse):
    units: list[Unit]


class Lesson(BaseModel):
    id: int
    steps: list[int]
    title: str


class LessonResponse(_BaseResponse):
    lessons: list[Lesson]


class Block(BaseModel):
    name: str
    text: str


class Step(BaseModel):
    id: int
    block: Block


class StepResponse(_BaseResponse):
    steps: list[Step]


class Reply(BaseModel):
    code: str = ""
    language: str


class Submission(BaseModel):
    id: int
    status: str
    reply: Reply


class SubmissionResponse(_BaseResponse):
    submissions: list[Submission]
