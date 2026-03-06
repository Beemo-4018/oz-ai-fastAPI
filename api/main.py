import anyio
from fastapi import (
    FastAPI,
    Path,
    Query,
    status,
    HTTPException,
    Depends,
    BackgroundTasks,
)
from typing import Optional
from schema import UserSignUpRequest, UserResponse, UserUpdateRequest

# from db_connection import SessionFactory, getSession
from db_models import User
from sqlalchemy import select
from sendEmail import send_email
from contextlib import asynccontextmanager
from mysql_connection import getSession
from async_mysql_connection import get_async_session


@asynccontextmanager
async def lifespan(_):
    # 서버 실행될 때, 실행되는 부분
    # limiter = anyio.to_thread.current_default_thread_limiter()
    # limiter.total_tokens = 200  # 스레드 풀 개수를 200개로 증량
    yield
    # 서버 종료될 때, 실행되는 부분


# lifespan -> FastAPI 서버가 실행되고 종료될 때, 특정 리소스를 생성하고 정리하는 기능
app = FastAPI(lifespan=lifespan)


@app.get("/")
async def roo_hd():
    return "test : good"


@app.get("/users", status_code=status.HTTP_200_OK, response_model=list[UserResponse])
async def get_users_handlers(
    # Depends
    # 요청시작 -> session 생성
    # 응답 반환 -> session.close()
    session=Depends(get_async_session),
):
    stmt = select(User)
    result = await session.execute(stmt)
    users = result.scalars().all()
    return users


# 회원가입 API
@app.post(
    "/users/signup",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponse,
)
async def signup_user_handler(
    body: UserSignUpRequest,
    background_tasks: BackgroundTasks,
    session=Depends(get_async_session),
):
    new_user = User(name=body.name, age=body.age, email=body.email)

    # DB 작업 단위
    session.add(new_user)  # 임시 저장
    await session.commit()  # DB에 저장

    # 이메일 전송 작업 BT 등록
    background_tasks.add_task(send_email, body.name)
    return new_user


# 회원 검색 API
@app.get("/users/search")
def search_users_handler(name: str):
    return {"message": f"회원 검색 API입니다. 검색어: {name}"}


# 단일 사용자 조회 API
# 설정	의미
# gt	Greater Than (> 초과)
# ge	Greater than or Equal to (≥ 이상)
# lt	Less Than (< 미만)
# le	Less than or Equal to (≤ 이하)
# title	문서에 표시될 제목
@app.get(
    "/users/{user_id}", status_code=status.HTTP_200_OK, response_model=UserResponse
)
def get_user_handler(
    user_id: int = Path(..., ge=1, description="사용자 ID는 1 이상이어야 합니다."),
    session=Depends(getSession),
):
    stmt = select(User).where(User.id == user_id)
    result = session.execute(stmt)
    user = result.scalar()

    if user is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail="존재하지 않는 사용자 ID입니다."
        )
    return user


# 사용자 정보 수정 API
@app.patch("/users/{user_id}")
async def update_user_handler(
    body: UserUpdateRequest,
    user_id: int = Path(..., ge=1, description="사용자 ID는 1 이상이어야 합니다."),
    session=Depends(get_async_session),
):
    if body.name is None and body.age is None:
        raise HTTPException(status_code=400, detail="업데이트할 정보가 없습니다.")

    stmt = select(User).where(User.id == user_id)
    result = await session.execute(stmt)
    user = result.scalar()

    if user is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail="존재하지 않는 사용자 ID입니다."
        )

    # 2) 사용자 정보 업데이트
    if body.name is not None:
        user.name = body.name
    if body.age is not None:
        user.age = body.age
    await session.commit()

    # 3) 업데이트된 사용자 정보 반환
    return user


# 사용자 삭제(회원탈퇴) API
@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_handler(
    user_id: int = Path(..., ge=1, description="사용자 ID는 1 이상이어야 합니다."),
    session=Depends(get_async_session),
):
    stmt = select(User).where(User.id == user_id)
    result = await session.execute(stmt)
    user = result.scalar()

    if user is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail="존재하지 않는 사용자 ID입니다."
        )

    session.delete(user)
    await session.commit()
    return None


# GET / items /{item_name}
# item_name: str & 최대 글자수(max_length) 6
items = [
    {"id": 1, "item_name": "apply"},
    {"id": 2, "item_name": "banana"},
    {"id": 3, "item_name": "cherry"},
]


# @app.get("/items/{item_name}")
# def get_item_handler(
#     item_name: str = Path(
#         ..., min_length=2, max_length=6, description="아이템 이름은 최대 6자입니다."
#     )
# ):
#     for item in items:
#         if item["item_name"] == item_name:
#             return item
#     return {"message": "아이템을 찾을 수 없습니다."}


@app.get("/items/search")
def search_items_handler(
    item_name: str = Query(
        ...,
        min_length=2,
        max_length=6,
        description="아이템 이름은 최대 6자입니다.",  # ... 필수값
    ),
    age: Optional[int] = Query(
        None, ge=0, description="나이는 0 이상이어야 합니다."
    ),  # Optional 선택값
):
    return item_name, age
