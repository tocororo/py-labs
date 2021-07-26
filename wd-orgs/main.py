import uvicorn
from fastapi import FastAPI

from Database.instanceOfDao import InstanceOfDao

app = FastAPI()


@app.get("/entities")
async def getEntities():
    data = await InstanceOfDao.createJson()
    return data


@app.post("/collect/")
async def startCollect(org: str):
    # await collect(org)
    return org


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=4000)
