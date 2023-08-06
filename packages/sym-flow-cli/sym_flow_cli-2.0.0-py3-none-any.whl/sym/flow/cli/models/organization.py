from typing import List, Optional

from pydantic import BaseModel


class Organization(BaseModel):
    slug: str
    client_id: Optional[str] = None
    domains: List[str] = []
