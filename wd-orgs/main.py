import uvicorn
from fastapi import FastAPI, Form

from Controllers.entities import Entities

app = FastAPI()


@app.get("/entities")
async def getEntities():
    data = await Entities.createJson()
    return data


@app.post("/collect/")
async def startCollect(org: str = Form(...)):
    # await collect(org)
    return org


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=4000)
