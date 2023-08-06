import datetime as dt
from typing import Union, List

from pydantic import BaseModel


class SearchInfo(BaseModel):
    class Config:
        validate_assignment = True

    A_title: str = None
    A_content: Union[str, List[str]] = None
    A_file_path_list: List[str] = []
    A_file_name_list: List[str] = []
    A_label_list: List[str] = []
    A_create_time: dt.datetime = None
