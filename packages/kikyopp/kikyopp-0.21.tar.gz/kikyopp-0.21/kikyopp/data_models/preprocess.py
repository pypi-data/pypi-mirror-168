import datetime as dt

from pydantic import BaseModel


class PreprocessResult(BaseModel):
    class Config:
        validate_assignment = True

    id: str = None
    data_source: str = None
    create_time: dt.datetime = None
    update_time: dt.datetime = None
