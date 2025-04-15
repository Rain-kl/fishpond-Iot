import uvicorn

if __name__ == "__main__":
    uvicorn.run("api:app", port=10086, reload=True)
