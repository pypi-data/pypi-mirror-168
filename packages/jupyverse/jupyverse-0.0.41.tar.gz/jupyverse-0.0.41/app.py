from datetime import datetime

from fastapi import Depends, FastAPI, HTTPException, Query, Request, Response, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import APIKeyCookie
from fief_client import FiefAsync, FiefUserInfo
from fief_client.integrations.fastapi import FiefAuth


class CustomFiefAuth(FiefAuth):  # !
    client: FiefAsync

    async def get_unauthorized_response(self, request: Request, response: Response):
        redirect_uri = request.url_for("auth_callback")  # !
        auth_url = await self.client.auth_url(redirect_uri, scope=["openid"])  # !
        raise HTTPException(
            status_code=status.HTTP_307_TEMPORARY_REDIRECT,  # !
            headers={"Location": auth_url},
        )


if True:
    fief = FiefAsync(  # !
        "http://localhost:8000",
        "UHb6_l_1nrmJZY3749ympehvpwlVz28UYM_raRRvTg8",
        "LlwOVy-CTKaI7HHwz03LRyEIWFf_5s4QbquI3NX9Lng",
    )
else:
    fief = FiefAsync(
        "https://jupyverse.fief.dev",
        "cRe7WP-zstMx7j9KtDLjwrET2LD94mjGuqm4D4A9LZw",
        "IGyIgF361NRC_ZxN7pheYwqrTTsdldTq4tNlm6QxzlM",
    )

SESSION_COOKIE_NAME = "user_session"
scheme = APIKeyCookie(name=SESSION_COOKIE_NAME, auto_error=False)  # !
auth = CustomFiefAuth(fief, scheme)  # !
app = FastAPI()


@app.get("/auth-callback", name="auth_callback")  # !
async def auth_callback(request: Request, response: Response, code: str = Query(...)):
    redirect_uri = request.url_for("auth_callback")
    #print(f"{redirect_uri=}")
    tokens, _ = await fief.auth_callback(code, redirect_uri)  # !
    #print(f"{tokens=}")
    #print(f"{request.url_for('protected')=}")

    response = RedirectResponse(request.url_for("protected"))  # !
    response.set_cookie(  # !
        SESSION_COOKIE_NAME,
        tokens["access_token"],
        expires=int(datetime.now().timestamp() + tokens["expires_in"]),
        httponly=True,  # !
        secure=False,  # ❌ Set this to `True` in production !
    )

    return response


@app.get("/protected", name="protected")
async def protected(
    request: Request, 
    user: FiefUserInfo = Depends(auth.current_user()),  # !
):
    print(f"{request._cookies=}")
    return HTMLResponse(
        f"<h1>You are authenticated. Your user email is {user['email']}</h1>"
    )
