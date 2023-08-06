import context
from fastapi import FastAPI

# import uvicorn

# import uvicorn
from api.routers import user, case, authentication

app = FastAPI()

app.include_router(authentication.router)
app.include_router(user.router)
app.include_router(case.router)

# uvicorn.run(app, host="localhost", port=8000)
