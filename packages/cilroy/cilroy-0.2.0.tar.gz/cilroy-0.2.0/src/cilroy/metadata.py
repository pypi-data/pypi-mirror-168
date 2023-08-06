from pydantic import BaseModel


class Metadata(BaseModel):
    key: str
    description: str
