from fastapi import FastAPI, Request, Form, Query
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app import crud
from app.models import Entry, Example
from datetime import datetime

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request, q: str = Query(None), field: str = Query("word")):
    entries = crud.get_all_entries()
    filtered = []

    if q:
        for entry in entries:
            value = entry.get(field, "")
            if isinstance(value, list):
                value = " ".join(value)
            if q.lower() in value.lower():
                filtered.append(entry)
    else:
        filtered = entries

    return templates.TemplateResponse("index.html", {
        "request": request,
        "entries": filtered,
        "q": q,
        "field": field,
        "year": datetime.now().year
    })

@app.get("/entries/new", response_class=HTMLResponse)
async def new_entry_form(request: Request):
    return templates.TemplateResponse("entry_form.html", {"request": request, "year": datetime.now().year})

@app.post("/entries")
async def create_entry(
    word: str = Form(...),
    part_of_speech: str = Form(...),
    definition: str = Form(...),
    tok_pisin: str = Form(""),
    example_kamano: str = Form(""),
    example_english: str = Form("")
):
    example = None
    if example_kamano and example_english:
        example = Example(kamano=example_kamano, english=example_english)
    entry = Entry(
        word=word,
        part_of_speech=part_of_speech,
        definition=definition,
        tok_pisin=tok_pisin,
        example=example
    )
    crud.create_entry(entry)
    return RedirectResponse(url="/", status_code=303)

@app.get("/entries/{word}", response_class=HTMLResponse)
async def entry_detail(request: Request, word: str):
    entry = crud.get_entry(word)
    return templates.TemplateResponse("entry_detail.html", {"request": request, "entry": entry, "year": datetime.now().year})
