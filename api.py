from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Expense API is running"}

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/hello/{name}")
async def hello(name: str):
    return {"message": f"Hello, {name}!"}