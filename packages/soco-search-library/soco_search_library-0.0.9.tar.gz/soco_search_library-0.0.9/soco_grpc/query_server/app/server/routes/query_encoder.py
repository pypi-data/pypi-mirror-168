from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from soco_grpc.query_server.app.server.models.data_manager import (
    PluginIn,
    PluginOut
)
from plugin_class import PluginClass

router = APIRouter()
pc = PluginClass()


@router.post("/plugin", name="plugin_call")
def clip_text(x: PluginIn = Body(...)) :
    x = jsonable_encoder(x)
    return PluginOut(resp=pc.plugin_method(x["data"]))
