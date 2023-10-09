from typing import List
from fastapi import FastAPI, HTTPException
import pandas as pd
from pydantic import BaseModel

from .model import get_model

app = FastAPI()

model = get_model()


class Flight(BaseModel):
    OPERA: str
    TIPOVUELO: str
    MES: int


class Flights(BaseModel):
    flights: List[Flight]


@app.get("/health", status_code=200)
async def get_health() -> dict:
    return {"status": "OK"}


@app.post("/predict", status_code=200)
async def post_predict(flights: Flights) -> dict:
    flights_list = flights.dict().get("flights")
    for flight in flights_list:
        # Run validations
        if flight.get("TIPOVUELO") not in ["N", "I"]:
            raise HTTPException(
                status_code=400, detail="'Tipo Vuelo' must be 'N' or 'I'."
            )
        if not 1 <= flight.get("MES") <= 12:
            raise HTTPException(
                status_code=400,
                detail="'Mes' must be greater or equal than 1 and less or equal than 12",
            )
    df_flights = pd.DataFrame(flights_list)
    features = model.preprocess(data=df_flights)
    predictions = model.predict(features=features)
    return {"predict": predictions}
