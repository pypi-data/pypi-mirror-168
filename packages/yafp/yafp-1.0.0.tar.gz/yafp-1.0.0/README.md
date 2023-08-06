## Yet another FastAPI profiler 🔧

FastAPI request profiler with the following features:

* #### 📄 Sort result by number of calls, filename or time
* #### ❌ Get rid of looking at fast calls, filter by minimal elapsed time to log the call
* #### ⚙️ Ignore python internals in log
* #### 🖌️ Pass custom logger to customize the log
* #### 📋 Apply profiler to only needed endpoints

---

### ⚠️ Python 3.10+ required

---

### Installation

`$ pip install yet-another-fastapi-profiler`

---

### Examples

```python
import time

import uvicorn
from fastapi import FastAPI

from yet_another_fastapi_profiler.middleware import ProfilerMiddleware, ProfilerMiddlewareSortOption

app = FastAPI()

app.add_middleware(
    ProfilerMiddleware,
    sort_by=ProfilerMiddlewareSortOption.CUMULATIVE,  # Sort option
    minimal_cumulative_time_to_print=1,  # Log functions which run more than 1 seconds
    ignore_python_internals=True,  # Ignore methods such as len(), __str__(), etc
    endpoints_to_measure=('/',)
)


def very_complex_logic():
    time.sleep(2)


@app.get("/")
async def long_endpoint():
    very_complex_logic()
    return {"too much": "time"}


@app.get("/no_need_to_profile")
async def short_endpoint():
    return {"so fast": "endpoint"}


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=12334,
        reload=True,
        debug=False
    )
```

gives you

```
INFO:     127.0.0.1:54728 - "GET / HTTP/1.1" 200 OK
GET / 2.00, 200
/home/user/fastapi-profiler/main.py:23 (long_endpoint) 1 0.00 2.00
/home/user/fastapi-profiler/main.py:19 (very_complex_logic) 1 0.00 2.00
```

---

### License

MIT

