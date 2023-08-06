from typing import Optional, List, Dict
from pydantic import BaseModel, Field


class PluginOut(BaseModel):
    resp: Optional[list]


class PluginIn(BaseModel):
    data: Optional[list]


class TokenizerIn(BaseModel):
    text: Optional[str]
    model_id: Optional[str]


class ImageBody(BaseModel):
    url: Optional[str]
    lang: Optional[str]


class TextBody(BaseModel):
    text: Optional[str]
    lang: Optional[str]


class TSSBody(BaseModel):
    tss: Optional[dict]


class ListIDs(BaseModel):
    data: list
    index_id: Optional[str]


class RemoveDocBody(BaseModel):
    ids: List
    index_id: Optional[str]
    collection_name: Optional[str]


class WriteDocBody(BaseModel):
    docs: List
    index_id: Optional[str]
    collection_name: Optional[str]


class ReadDocBody(BaseModel):
    index_id: Optional[str]


class UpdateModel(BaseModel):
    index_id: Optional[str]
    collection_name: Optional[str]
    query: Optional[dict]
    update: Optional[dict]


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(status, code, message):
    return {"status": status, "code": code, "message": message}


def SimpleResponseModel(status, code, message):
    return {"status": status, "code": code, "message": message}
