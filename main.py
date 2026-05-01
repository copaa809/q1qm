from fastapi import FastAPI, UploadFile, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from limiter import check_and_increment, get_count
from notifier import notify
from processor import download_audio, transcribe
import requests, os
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()
DEEPSEEK = os.getenv("DEEPSEEK_KEY")
total_visits = 0

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

def ask_deepseek(text: str) -> str:
    res = requests.post("https://api.deepseek.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {DEEPSEEK}"},
        json={"model": "deepseek-chat", "messages": [
            {"role": "system", "content": "أنت أستاذ جامعي تحلل المحاضرات بشكل احترافي"},
            {"role": "user", "content": f"""
افرز الشرح بالترتيب المشروح فيه بشكل واضح وجميل،
اشرح كل موضوع وارتبط بباقي المحاضرة،
اعمل مخطط شامل،
اكتب 5+ أسئلة تدريبية:

{text}
"""}
        ]})
    return res.json()["choices"][0]["message"]["content"]

@app.post("/process")
async def process(request: Request, url: str = Form(None), file: UploadFile = None):
    global total_visits
    ip = request.client.host

    if not check_and_increment(ip):
        return {"error": "وصلت الحد اليومي (3 محاضرات). ارجع غداً"}

    total_visits += 1
    count = get_count(ip)

    if url:
        if "youtube" in url or "youtu.be" in url:
            audio = download_audio(url)
        elif "zoom" in url:
            return {"error": "Zoom: حمّل التسجيل وارفعه كملف"}
        else:
            return {"error": "غير مدعوم هذا الرابط حاليا"}
    elif file:
        path = f"/tmp/{file.filename}"
        with open(path, "wb") as f:
            f.write(await file.read())
        audio = path
    else:
        return {"error": "أرسل رابطاً أو ملفاً"}

    text = transcribe(audio)
    result = ask_deepseek(text)
    notify(ip, count, total_visits)
    return {"result": result, "remaining": 3 - count}

@app.get("/stats")
async def stats():
    return {"total_visits": total_visits}