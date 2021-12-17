#!/usr/bin/python3
from aiohttp import web
import os
import zlib
import hashlib
from littlefs import LittleFS

async def handle(request):
    out_headers = {}
    out_data = None
    compress = False
    req_name = request.match_info.get('file')
    if req_name.endswith("python_boot.bin"):
        req_name = "python_boot.bin"
    if req_name.endswith("micropython.bin"):
        req_name = "micropython.bin"

    full_path = os.path.join("..", req_name)
    if full_path.endswith(".bin.gz"):
        extenson = ".bin.gz"
        root_path = full_path.removesuffix(".bin.gz")
    elif full_path.endswith(".bin"):
        extenson = ".bin"
        root_path = full_path.removesuffix(".bin")
    else:
        root_path = full_path

    print(req_name)

    if os.path.isdir(root_path):
        fs = LittleFS(block_size=4096, block_count=120)
        for root, _, files in os.walk(root_path, topdown=False):
            for name in files:
                path = os.path.join(root, name)
                with fs.open(name, 'w') as fh:
                    fh.write(open(path,"rb").read())
        out_data = fs.context.buffer
        if extenson.endswith(".gz"):
            compress = True
    elif os.path.isfile(full_path):
        out_data = open(full_path, "rb").read()
    else:
        print(f"File {full_path} not found (root {root_path})")

    if out_data is not None:
        if 'Range' in request.headers and "bytes=" in request.headers['Range']:
            print("Range only")
            byte_from_str, byte_to_str = request.headers['Range'].split("bytes=")[-1].split("-")
            byte_from, byte_to = int(byte_from_str), int(byte_to_str)
            out_headers['Content-Range'] = f'bytes {byte_from}-{byte_to}/{len(out_data)}'
            out_headers['Content-Length'] = f'{byte_to-byte_from}'
            print(request.headers['Range'])
            print(byte_from, byte_to)
            out_data = out_data[byte_from:byte_to]

        if 'Accept-Encoding' in request.headers and "gzip" in request.headers['Accept-Encoding']:
            print("Gzip on")
            compress = True

        if compress == True:
            print("Compressing")
            compress = zlib.compressobj(level=9, wbits=16 + 15)
            out_data = compress.compress(out_data)
            out_data += compress.flush(zlib.Z_FINISH)
            out_headers['Content-Encoding'] = 'gzip'

        return web.Response(body=out_data, headers=out_headers)

app = web.Application()
app.router.add_get('/{file}', handle)

web.run_app(app)
