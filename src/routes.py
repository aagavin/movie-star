from typing import Tuple

from starlette.routing import Mount
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from src.api.search import SearchRouter
from src.api.account import AccountRouter
from src.api.media import MediaRouter
from . import config, reqXSession
from .db import RedisDatabase


DEBUG = config('DEBUG', cast=bool)
app: Starlette = Starlette(debug=DEBUG)


async def startup():
    await RedisDatabase.open_database_connection_pool()


async def shutdown():
    await RedisDatabase.close_database_connection_pool()
    print('closing httpx session')
    await reqXSession.close()
    print('httpx session closed')


async def json_exception(request: Request, exc, status_code: int, custom_exceptions: Tuple):
    resp_obj = {
        'headers': request.headers.raw,
        'path': request.scope['raw_path'].decode("utf-8"),
        'status_code': status_code
    }
    if isinstance(exc, custom_exceptions):
        resp_obj['error'] = str(exc)
    else:
        resp_obj['error'] = exc.detail
        resp_obj['status_code'] = exc.status_code
    return JSONResponse(resp_obj, status_code=resp_obj['status_code'])


async def http_500_json_exception(request: Request, exc):
    return await json_exception(request, exc,  500, (ValueError, TypeError, KeyError))


async def http_404_json_exception(request: Request, exc):
    return await json_exception(request, exc, 404, (LookupError, ))


app.add_event_handler('startup', startup)
app.add_event_handler('shutdown', shutdown)
app.add_exception_handler(500, http_500_json_exception)
app.add_exception_handler(404, http_404_json_exception)

for error in [LookupError]:
    app.add_exception_handler(error, http_404_json_exception)

# add all 500 errors
for error in [ValueError, TypeError, KeyError]:
    app.add_exception_handler(error, http_500_json_exception)

app.routes.extend(
    [
        Mount('/search', app=SearchRouter),
        Mount('/media', app=MediaRouter),
        Mount('/user', app=AccountRouter)
    ]
)


@app.route('/')
async def home(request: Request) -> JSONResponse:
    return JSONResponse({'success': True, 'query': dict(request.query_params)})
