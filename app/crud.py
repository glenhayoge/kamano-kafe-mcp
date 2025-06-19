from fastapi import HTTPException
from app.models import Entry
from app.storage import load_data, save_data

def get_all_entries():
    return load_data()

def get_entry(word: str):
    data = load_data()
    for entry in data:
        if entry["word"] == word:
            return entry
    raise HTTPException(status_code=404, detail="Word not found")

def create_entry(entry: Entry):
    data = load_data()
    if any(e["word"] == entry.word for e in data):
        raise HTTPException(status_code=400, detail="Word already exists")
    data.append(entry.dict())
    save_data(data)
    return entry

def update_entry(word: str, entry: Entry):
    data = load_data()
    for i, e in enumerate(data):
        if e["word"] == word:
            data[i] = entry.dict()
            save_data(data)
            return entry
    raise HTTPException(status_code=404, detail="Word not found")

def delete_entry(word: str):
    data = load_data()
    new_data = [e for e in data if e["word"] != word]
    if len(new_data) == len(data):
        raise HTTPException(status_code=404, detail="Word not found")
    save_data(new_data)
    return {"message": f"Deleted {word}"}
