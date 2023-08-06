from fastapi import APIRouter

from server.app.server.models.heartbeat import Heartbeat

router = APIRouter()


@router.get("/ping", response_model=Heartbeat, name="ping")
def get_hearbeat() -> Heartbeat:
    heartbeat = Heartbeat(is_alive=True)
    return heartbeat


