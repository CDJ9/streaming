from fastapi import FastAPI

app = FastAPI()

@app.post("/test-post")
def test_post():
    return {"message": "POST request successful"}
