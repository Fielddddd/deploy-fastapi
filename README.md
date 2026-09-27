# FARMFORECAST — Backend

A FastAPI service that predicts vegetable sales weight for a given month from historical sales data. Used by the [front-farmforecast](https://github.com/Fielddddd/front-farmforecast) frontend.

## How it works

1. Client uploads a CSV of historical sales data via `POST /upload_csv`
2. The API forwards the file to a remote prediction model server
3. The model's prediction is returned to the client as JSON

## Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/` | Health check |
| GET | `/api` | Health check, returns `{"message": "OK"}` |
| POST | `/upload_csv` | Accepts a CSV file, forwards it to the model server, returns the prediction |

## Stack

Python, FastAPI, Uvicorn, deployed on Vercel

## Run locally

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```
