from fastapi import FastAPI
from controller import router

app = FastAPI(title="E-Commerce Coupon Engine")

# Connect the controller logic to the main app
app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Coupon API! Go to /docs to test it."}