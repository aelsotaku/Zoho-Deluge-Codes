from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Text,Optional
from datetime import datetime
from uuid import uuid4 as uuid

app = FastAPI()

publications = []

class Publication(BaseModel):
    id: Optional[str] = None
    title: str
    author: str
    content: Text
    created_at: datetime=datetime.now()
    published_at: Optional[datetime] = None
    published: bool = False


@app.get('/')
def read_root():
    return {"Welcome" : "Hola, bienvenidos a la nueva API Zoho/Demo QEngine"}

@app.get('/publications')
def get_publications():
    return publications


@app.get('/publicationss/{publication_id}')
def get_publication(publication_id: str):
    #print(publication_id)
    for publication in publications:
        if publication["id"] == publication_id:
            return publication
    raise HTTPException(status_code=404, detail="Publication not Found")


@app.post('/publications')
def save_publication(publication:Publication):

    publication.id=str(uuid())
    #print(uuid())
    
    publications.append(publication.model_dump())
    #print(publication.model_dump())
    return publications[-1]


@app.put('/publications/{publication_id}')
def update_publication(publication_id: str, updatePublication: Publication):
    for index, publication in enumerate(publications):
        if publication["id"] == publication_id:
            publications[index]["title"] = updatePublication.title
            publications[index]["content"] = updatePublication.content
            publications[index]["author"] = updatePublication.author
            return {"message" : "Publication has been updated successfully"}
    raise HTTPException(status_code=404, detail="Publication not Found")


@app.delete('/publications/{publication_id}')
def delete_publication(publication_id: str):
    for index, publication in enumerate(publications):
        if publication["id"] == publication_id:
            publications.pop(index)
            return {"message" : "Publication has been deleted successfully"}
    raise HTTPException(status_code=404, detail="Publication not Found")

