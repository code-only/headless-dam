from fastapi import FastAPI, Depends
from dependencies.auth import get_current_user
from db import engine, Base
from routers import (
    auth,
    users,
    assets,
    metadata,
    tags,
    search,
    permissions,
    audit,
    lifecycle,
    webhooks,
    reports,
    misc,
    transform,
)

import models

app = FastAPI(title="Headless DAM API")


@app.on_event("startup")
def on_startup():
    # This will create all tables if they do not exist
    Base.metadata.create_all(bind=engine)


app.include_router(auth.router, prefix="/auth", tags=["Authentication"])

# Protected routers (with auth)
app.include_router(
    users.router,
    prefix="/users",
    tags=["Users"],
    dependencies=[Depends(get_current_user)],
)
app.include_router(
    assets.router,
    prefix="/assets",
    tags=["Assets"],
    dependencies=[Depends(get_current_user)],
)
app.include_router(
    metadata.router,
    prefix="/metadata",
    tags=["Metadata"],
    dependencies=[Depends(get_current_user)],
)
app.include_router(
    tags.router, prefix="/tags", tags=["Tags"], dependencies=[Depends(get_current_user)]
)
app.include_router(
    transform.router,
    prefix="/transform",
    tags=["Transform"],
    dependencies=[Depends(get_current_user)],
)
app.include_router(
    search.router,
    prefix="/search",
    tags=["Search"],
    dependencies=[Depends(get_current_user)],
)
app.include_router(
    permissions.router,
    prefix="/permissions",
    tags=["Permissions"],
    dependencies=[Depends(get_current_user)],
)
app.include_router(
    audit.router,
    prefix="/audit",
    tags=["Audit"],
    dependencies=[Depends(get_current_user)],
)
app.include_router(
    lifecycle.router,
    prefix="/assets",
    tags=["Lifecycle"],
    dependencies=[Depends(get_current_user)],
)
app.include_router(
    webhooks.router,
    prefix="/webhooks",
    tags=["Webhooks"],
    dependencies=[Depends(get_current_user)],
)
app.include_router(
    reports.router,
    prefix="/reports",
    tags=["Reports"],
    dependencies=[Depends(get_current_user)],
)
app.include_router(misc.router, tags=["Misc"], dependencies=[Depends(get_current_user)])

