from api import app
import uvicorn

# To do:
# 1. Encrypt data
# 2. For new users, send an email

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)

# import uvicorn

# if __name__ == "__main__":
#     uvicorn.run("api:app", host="0.0.0.0", port=8001, reload=True)