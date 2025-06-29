from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from openai import OpenAI
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/", StaticFiles(directory="static", html=True), name="static")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class RequestData(BaseModel):
    text: str

@app.post("/catalog")
async def catalog_book(request_data: RequestData):
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a MARC21 cataloging assistant. Use RDA rules."},
                {"role": "user", "content": request_data.text}
            ],
            temperature=0.5,
            max_tokens=2048
        )
        result = response.choices[0].message.content.strip()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@app.get("/ping")
async def ping():
    return {"message": "GPT Cataloging API is live"}
