from aiohttp import web
import os
import hashlib


async def handle(request):
    name = request.match_info.get('file')
    path = os.path.join("..", name)
    print(path)
    if os.path.isfile(path):
        print("here")
        file_data = open(path, "rb").read()
        sha = hashlib.sha224(file_data).hexdigest()
        return web.Response(body=file_data, headers={"etag": sha})

app = web.Application()
app.router.add_get('/{file}', handle)

web.run_app(app)
