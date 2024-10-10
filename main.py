import requests
import logging
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# ตั้งค่า logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# URL ของโมเดลที่ deploy
MODEL_URL = "http://54.91.48.234:5000/train"  # เปลี่ยนเป็น URL ของโมเดลคุณ

@app.get("/")
async def root():
    return {"message": "Hello from FastAPI on Vercel"}

# เส้นทางใหม่ /api ตอบกลับ "OK"
@app.get("/api")
async def get_api():
    return JSONResponse(content={"message": "OK"})

@app.post("/upload_csv")
async def upload_csv(file: UploadFile = File(...)):
    logger.info("Received file: %s", file.filename)

    # ตรวจสอบประเภทไฟล์
    if file.content_type != 'text/csv':
        logger.error("File type is not CSV: %s", file.content_type)
        raise HTTPException(status_code=400, detail="Only CSV files are accepted.")

    contents = await file.read()
    logger.info("File content size: %d bytes", len(contents))

    # ส่งไฟล์ไปยังโมเดล
    try:
        response = requests.post(MODEL_URL, files={"file": (file.filename, contents, "text/csv")})
        logger.info("Model response status code: %d", response.status_code)
    except Exception as e:
        logger.error("Error while sending request to model: %s", str(e))
        raise HTTPException(status_code=500, detail="Error occurred while sending request to model.")

    # ตรวจสอบสถานะการตอบกลับจากโมเดล
    if response.status_code != 200:
        logger.error("Model returned non-200 status: %s", response.status_code)
        raise HTTPException(status_code=response.status_code, detail=response.json().get("detail", "Error occurred while predicting."))
    
    logger.info("Model response: %s", response.json())

    return JSONResponse(content=response.json())
