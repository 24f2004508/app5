from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uuid

app = FastAPI()

API_KEY = "ak_mvafua5czqclbmgqobxf9ob8"

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://exam.sanand.workers.dev",
        "https://app-7tq7pw.example.com"
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analytics")
async def analytics(request: Request):
    # Auth check
    api_key = request.headers.get("X-API-Key")
    if api_key != API_KEY:
        return JSONResponse(status_code=401, content={"detail": "Unauthorized"})

    data = await request.json()
    events = data.get("events", [])

    total_events = len(events)
    users = {}
    for e in events:
        user = e.get("user")
        amt = e.get("amount", 0)
        if amt > 0:
            users[user] = users.get(user, 0) + amt

    unique_users = len(set(e.get("user") for e in events))
    revenue = sum(e.get("amount", 0) for e in events if e.get("amount", 0) > 0)
    top_user = max(users, key=users.get) if users else None

    return {
        "email": "24f2004508@ds.study.iitm.ac.in",
        "total_events": total_events,
        "unique_users": unique_users,
        "revenue": revenue,
        "top_user": top_user,
    }
