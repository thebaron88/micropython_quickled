from aiohttp import web
import os
import zlib
import hashlib
from littlefs import LittleFS

async def handle(request):
    name = request.match_info.get('file')
    path = os.path.join("..", name)
    print(path)
    if os.path.isfile(path):
        print("here")
        file_data = open(path, "rb").read()
        sha = hashlib.sha224(file_data).hexdigest()
        return web.Response(body=file_data, headers={"ETag": sha})
    if name == "DYNAMIC.bin.gz":
        fs = LittleFS(block_size=4096, block_count=120)
        for root, _, files in os.walk("../python", topdown=False):
            for name in files:
                path = os.path.join(root, name)
                with fs.open(name, 'w') as fh:
                    fh.write(open(path,"rb").read())
        compress = zlib.compressobj(level=9, wbits=16 + 15)
        file_data = compress.compress(fs.context.buffer)
        file_data += compress.flush(zlib.Z_FINISH)
        sha = hashlib.sha224(file_data).hexdigest()
        print(f"Sending {len(file_data)} bytes")
        return web.Response(body=file_data, headers={"ETag": sha})


app = web.Application()
app.router.add_get('/{file}', handle)

web.run_app(app)
