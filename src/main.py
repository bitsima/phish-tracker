import uvicorn

from api import routes


if __name__ == "__main__":
    uvicorn.run(routes.app, host="localhost", port=8000)
