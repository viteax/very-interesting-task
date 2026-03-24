from pydantic import BaseModel


class CodeProblem(BaseModel):
    title: str
    description: str


class CodeSolution(BaseModel):
    title: str
    description: str
    img_path: str
