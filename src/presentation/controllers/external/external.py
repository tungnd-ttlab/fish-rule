from typing import Annotated
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Query
from dishka import FromDishka

from application.interactors.external.delete_file import DeleteFileInteractor, DeleteFileRequest
from application.interactors.external.list_file import (
    ListFileRequest,
    ListFileResponse,
    ListFileInteractor,
)
from application.interactors.external.postfile import (
    PostFileRequest,
    PostFileResponse,
    PostFileInteractor,
)
from presentation.constants import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    ERROR_BAD_REQUEST,
)

router = APIRouter(prefix="/external", tags=["external"])


@router.post(
    "/img",
    status_code=HTTP_200_OK,
    responses={
        HTTP_400_BAD_REQUEST: {"description": ERROR_BAD_REQUEST},
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
    status_code=HTTP_200_OK,
    responses={
        HTTP_400_BAD_REQUEST: {"description": ERROR_BAD_REQUEST},
    },
)
@inject
async def listImg(
    data: Annotated[ListFileRequest, Query()],
    list_file: FromDishka[ListFileInteractor],
) -> ListFileResponse:
    return await list_file(data)


@router.delete(
    "/img/{file_id}",
    status_code=HTTP_200_OK,
    responses={
        HTTP_400_BAD_REQUEST: {"description": ERROR_BAD_REQUEST},
    },
)
@inject
async def deleteImg(
    file_id: int,
    delete_file: FromDishka[DeleteFileInteractor],
) -> None:
    await delete_file(DeleteFileRequest(file_id=file_id))