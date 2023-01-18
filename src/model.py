from typing import Dict
from pydantic import BaseModel
from datetime import datetime

class Note:
    def __init__(self, note_id, text, created_time, updated_time):
        self.note_id = note_id
        self.text = text
        self.created_time = created_time
        self.updated_time = updated_time

    def update(self, text, update_at):
        self.text = text
        self.updated_time = update_at

class GetNoteInfo(BaseModel):
    created_at: datetime
    updated_at: datetime

class GetNoteText(BaseModel):
    id: int
    text: str

class CreateNote(BaseModel):
    id: int

class DeleteNote(BaseModel):
    removed_id: int

class UpdateNote(BaseModel):
    id: int
    text: str

class GetNotesList(BaseModel):
    notes_list: Dict[int, int]