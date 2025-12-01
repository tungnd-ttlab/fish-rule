from typing import Annotated
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Body, Query
from starlette import status

from dishka import FromDishka

from application.interactors.external.delete_file import DeleteFileInteractor, DeleteFileRequest
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
    data: Annotated[ListFileRequest , Query()],
    list_file: FromDishka[ListFileInteractor],
) -> ListFileResponse:
    return await list_file(data)

@router.delete(
    "/img/{file_id}",
    status_code=status.HTTP_200_OK,
    responses={
        400: {"description": "Bad Request"},
    },
)
@inject
async def deleteImg(
    file_id: int,
    delete_file: FromDishka[DeleteFileInteractor],
) -> None:
    await delete_file(DeleteFileRequest(file_id=file_id))