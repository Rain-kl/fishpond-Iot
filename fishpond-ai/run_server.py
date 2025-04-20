import uvicorn

from api import app

if __name__ == "__main__":
    # uvicorn.run("api:app", port=10086)
    uvicorn.run(app, host="0.0.0.0", port=10099)
