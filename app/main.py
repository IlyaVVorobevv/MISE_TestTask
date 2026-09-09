from fastapi import FastAPI
from app.api.bookings import router_booking


app = FastAPI(title="Booking App")

app.include_router(router_booking)

@app.get("/", include_in_schema=False)
async def root() -> dict[str, str]:
    return {"status": "ok", "docs": "/docs"}