from fastapi import APIRouter

router = APIRouter(
    prefix='/director',
    tags=['songs']
)


@router.post("/common_playlist")
async def create_common_playlist():
    raise NotImplementedError


@router.get('/common_playlist/all')
async def get_common_playlists():
    raise NotImplementedError
