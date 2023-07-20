from pydantic import Field, BaseModel


class Table(BaseModel):
    id: str = ''
    person_count: int = Field(include=True)