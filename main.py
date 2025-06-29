
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import openai
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

openai.api_key = os.getenv("OPENAI_API_KEY")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def serve_index():
    return FileResponse("static/index.html")

@app.post("/catalog")
async def catalog_books(request: Request):
    data = await request.json()
    user_input = data.get("text", "")

    system_prompt = "📚 You are a cataloging assistant. Convert any book description into MARC21 RDA format. Provide detailed fields."

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            { "role": "system", "content": system_prompt },
            { "role": "user", "content": user_input }
        ]
    )

    return { "result": response["choices"][0]["message"]["content"] }
