
from controllers import chatuol
from fastapi import FastAPI
import uvicorn


# initialize FastApi
app = FastAPI()
app.include_router(chatuol.router, prefix="/chatuol",
                   tags=["AvgPrice & Tax"])

# run uvicorn
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=9000, reload=True)
