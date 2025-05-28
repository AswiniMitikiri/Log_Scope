from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from parser import parse_access_log, parse_error_log, parse_fallback
import os, shutil

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload/")
async def upload_log(file: UploadFile = File(...)):
    os.makedirs("logs", exist_ok=True)
    file_path = f"logs/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    with open(file_path, "r") as f:
        sample_lines = [f.readline() for _ in range(5)]
    log_format = "access" if any("GET" in line and "HTTP" in line for line in sample_lines) else "error"

    if log_format == "access":
        parsed_data = parse_access_log(file_path)
    else:
        parsed_data = parse_error_log(file_path)

    if not parsed_data:
        parsed_data = parse_fallback(file_path)

    return {
        "filename": file.filename,
        "parsed_entries": len(parsed_data),
        "logs": parsed_data
    }
