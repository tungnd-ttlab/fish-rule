from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Body
from starlette import status

from dishka import FromDishka

from application.interactors.external.list_file import (ListFileRequest, ListFileResponse ,ListFileInteractor)
from application.interactors.external.postfile import (
    PostFileRequest,
    PostFileResponse,
    PostFileInteractor,
)

router = APIRouter(prefix="/external", tags=["external"])


@router.post(
    "/img",
    status_code=status.HTTP_200_OK,
    responses={
        400: {"description": "Bad Request"},
    },
)
@inject
async def postImg(
    data: PostFileRequest,
    post_file: FromDishka[PostFileInteractor],
) -> PostFileResponse:
    return await post_file(data)

@router.get(
    "/img",
    status_code=status.HTTP_200_OK,
    responses={
        400: {"description": "Bad Request"},
    },
)
@inject
async def listImg(
    data: ListFileRequest,
    list_file: FromDishka[ListFileInteractor],
) -> ListFileResponse:
    return await list_file(data)