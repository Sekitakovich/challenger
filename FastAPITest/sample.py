from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel

app = FastAPI()


class User(BaseModel):
    ID: int
    name: str


@app.post(f"/user")
def addUser(user: User):
    return {"res": "ok", "ID": user.ID, "名前": user.name}


@app.get("/")
def read_root():
    return {"Hello": "World"}


if __name__ == '__main__':
    def main():
        uvicorn.run(app=app, host='0.0.0.0', port=80)


    main()
