from fastapi import FastAPI

from .src.processor import process_repo_to_get_readme

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/readme")
async def get_readme(repo_link: str):
    print(repo_link)
    return await process_repo_to_get_readme(repo_link)
