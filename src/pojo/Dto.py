from typing import Any, List

from pydantic import BaseModel



class ResourceDto(BaseModel):
    page: int
    per_page: int
    total: int
    total_pages: int
    data: List[DataResourceDto]
    support: Any = None



class DataResourceDto(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    avatar: str
