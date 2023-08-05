# import os

import uvicorn
from app import app


@app.get("/")
async def root():
    return {"message": "Hello World"}


# and os.getenv("DEBUG", "0") == 1

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000, debug=True)
