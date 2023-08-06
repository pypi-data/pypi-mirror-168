from fief_client import Fief

fief = Fief(
    "http://localhost:8000",  # (1)!
    "QpXcpRqgpBGffIP61_jrELxD9z31ZNF91r8KLxbAUBk",  # (2)!
    "KPCmLCx8BxF2Y81gXo9pJC6oVMbpGqSiNXP0dBPuONM",  # (3)!
)

redirect_url = "http://localhost:8888/auth-callback"

auth_url = fief.auth_url(redirect_url, scope=["openid"])
print(f"Open this URL in your browser: {auth_url}")

code = input("Paste the callback code: ")

tokens, userinfo = fief.auth_callback(code, redirect_url)
print(f"Tokens: {tokens}")
print(f"Userinfo: {userinfo}")
