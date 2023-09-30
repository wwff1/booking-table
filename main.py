from fastapi import FastAPI
from routers import user, table, booking


app = FastAPI()
app.include_router(user.router)
app.include_router(table.router)
app.include_router(booking.router)
