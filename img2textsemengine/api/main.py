from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, RedirectResponse
from starlette_prometheus import PrometheusMiddleware, metrics
from img2textsemengine.api import lifespan
from img2textsemengine.api.routes import router


app = FastAPI(
    title='text 2 image search engine',
    description="This service is a Demo on how to use Clip model to build a text 2 image semantic search engine.",
    lifespan=lifespan
)


@app.exception_handler(ValueError)
async def value_error_exception_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={"message": str(exc)},
    )
app.include_router(router)


@app.get("/", summary="redirects to Swagger UI", include_in_schema=False)
def root():
    return RedirectResponse(url='/docs')


# Include Prometheus support
app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics", metrics)
