import uvicorn
from fastapi import FastAPI, Form

from Controllers.dataCollect import collect, getDataInstance
from Controllers.instance import Instance

app = FastAPI()


@app.get("/entities")
async def getEntities():
    data = await Instance.createJson()
    return data


@app.post("/collect/")
async def startCollect(org: str = Form(...)):
    await Instance.createTableInstance()
    await Instance.createTableSubclass()
    await collect(org)
    await getDataInstance('original')
    return org


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=4000)
