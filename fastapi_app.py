from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class PredictionRequest(BaseModel):
    text: str

# Модель ответа от сервера
class PredictionResponse(BaseModel):
    prediction: str

@app.get("/api/generate")
async def predict_text(request: PredictionRequest):
    prediction = "89"
    return {"prediction": str(prediction)}

