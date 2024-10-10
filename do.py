import requests
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

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

@app.post("/upload_csv")
async def upload_csv(file: UploadFile = File(...)):
    # ตรวจสอบประเภทไฟล์
    if file.content_type != 'text/csv':
        raise HTTPException(status_code=400, detail="Only CSV files are accepted.")

    contents = await file.read()

    # ส่งไฟล์ไปยังโมเดล
    response = requests.post(MODEL_URL, files={"file": (file.filename, contents, "text/csv")})

    # ตรวจสอบสถานะการตอบกลับจากโมเดล
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json().get("detail", "Error occurred while predicting."))
        
    return JSONResponse(content=response.json())
    
    # แสดงผลลัพธ์ที่ได้รับจากโมเดล
    #response_json = response.json()

# ตรวจสอบว่ามีคีย์ "predicted_sales"
    #if "predicted_sales" not in response_json:
        #raise HTTPException(status_code=500, detail="Invalid response from model.")

    #return JSONResponse(content={
        #"predictions": response_json.get("predicted_sales", []), 
        #"status": "success"
#})