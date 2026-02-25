from pydantic import BaseModel

class JobFeatures(BaseModel):
    location: str
    classification_sub: str
    work_type: str
    python: int
    llm: int
    data: int
    production: int
    ai: int
    sql: int
    cloud: int
    senior: int
    java: int
    javascript: int
    security: int