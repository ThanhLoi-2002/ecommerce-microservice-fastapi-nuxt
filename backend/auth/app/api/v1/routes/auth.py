import json
from fastapi import APIRouter, HTTPException, status
import httpx
from app.common.decorator.responseMessage import response_message
from app.api.v1.deps import AsyncSessionDep
from app.common.middleware.response_wrapper import ResponseInterceptorRoute
from app.core.security import createToken, decode_refresh_token, refreshToken, createRefreshToken
from app.crud.crud_user import crud_user
from app.schemas.user import UserResponse
from app.utils.hashPass import HashHelper
from ....schemas.auth import LoginDto, SignUpDto
from bs4 import BeautifulSoup

router = APIRouter(route_class=ResponseInterceptorRoute)


@router.post("/signin")
@response_message("Logged in")
async def signin(data: LoginDto, db: AsyncSessionDep):
    user = await crud_user.get_one(db, {"email": data.email})
    if not user or not HashHelper.verify_password(data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid email or password",
        )

    # create token
    payload = {"id": user.id}
    token = createToken(payload)
    refreshToken = createRefreshToken(payload)
    return {"token": token, "refreshToken": refreshToken}


@router.post("/signup", response_model=UserResponse)
@response_message("Sign up successfully")
async def signup(data: SignUpDto, db: AsyncSessionDep):
    user = await crud_user.get_one(db, {"email": data.email})
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email already exists"
        )

    return await crud_user.create(db, data)


@router.post("/refresh-token")
async def refreshTokenHandler(data: dict, db: AsyncSessionDep):
    refresh_token = data.get("refreshToken")

    if refresh_token == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Refresh token not found"
        )
    payload = decode_refresh_token(refresh_token)

    user = await crud_user.get_one(db, {"id": payload.get('id')})

    if user == None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Please login again"
        )

    token = refreshToken(refresh_token)
    if token == None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Please login again"
        )
    else:
        return {"token": token}

@router.get("/preview")
async def preview(url: str):
    async with httpx.AsyncClient(follow_redirects=True, timeout=5) as client:
        r = await client.get(url)

    soup = BeautifulSoup(r.text, "html.parser")
    # print(soup.prettify())

    def og(name):
        tag = soup.find("meta", property=f"og:{name}")
        return tag["content"] if tag else None

    return {
        "url": url,
        "title": og("title") or soup.title.string if soup.title else "",
        "description": og("description"),
        "image": og("image"),
        "site": og("site_name")
    }