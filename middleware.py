import time
from fastapi import Request
async def log_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    end = time.time()
    print(f"""
        METHOD: {request.method}
        PATH: {request.url.path}
        TIME: {end-start}
    """)
    return response