from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import openai, os

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def serve_index():
    return FileResponse("static/index.html")

@app.post("/catalog")
async def catalog(request: Request):
    data = await request.json()
    user_text = data.get("text", "")

    if not user_text:
        return JSONResponse({"error": "No text provided"}, status_code=400)

    openai.api_key = os.getenv("OPENAI_API_KEY")
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": user_text}]
        )
        result = completion.choices[0].message.content
        return {"result": result}
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
