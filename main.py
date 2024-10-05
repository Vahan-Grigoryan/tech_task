import uvicorn
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi import FastAPI
from api.auth.routes import router as auth_router
from api.cats.routes import router as cats_router
from core import config, utils


app = FastAPI(lifespan=utils.create_initial_data_for_testing)
app.include_router(auth_router)
app.include_router(cats_router)
settings = config.Settings()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    """
    Change fastapi default error message for be similar to HTTPException
    """
    errors = []
    for error in exc.errors():
        errors.append({
            "field": error["loc"][-1],
            "message": error["msg"]
        })
    raise HTTPException(
        status_code=400,
        detail=errors
    )


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=True,
        reload_delay=0
    )
