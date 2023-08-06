from fastapi import FastAPI

from soco_grpc.query_server.app.server.routes.query_encoder import router as QueryRouter

app = FastAPI()

app.include_router(QueryRouter, tags=["QueryManager"], prefix="/v1/query")


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this Soco-Search app!"}
