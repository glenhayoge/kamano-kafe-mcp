from pydantic import BaseModel
from typing import List, Optional

class Example(BaseModel):
    kamano: str
    english: str

class Entry(BaseModel):
    word: str
    part_of_speech: str
    definition: str
    variants: Optional[List[str]] = []
    tok_pisin: Optional[str] = ""
    example: Optional[Example] = None
