from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from typing import List, Dict, Any, Union, Optional
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# MongoDB connection
client = AsyncIOMotorClient(os.getenv("MONGODB_URL"))
db = client[os.getenv("MONGODB_DB")]
collection = db[os.getenv("MONGODB_COLLECTION")]

class ParticipantInfo(BaseModel):
    name: str
    age: int
    gender: str
    phone: str
    catchTrialCorrect: Optional[str] = None
    experimentStartDateTime: Optional[str] = None
    experimentEndDateTime: Optional[str] = None
    experimentDuration: Optional[int] = None

class TrialData(BaseModel):
    trial_id: int
    trial_type: str
    image1_id: Union[int, str]
    image2_id: Union[int, str]
    selected_index: int
    selected_image_id: Union[int, str]
    reaction_time: int
    timestamp: int
    catch_trial_correct: Optional[str] = None
    trial_start_datetime: Optional[str] = None
    trial_end_datetime: Optional[str] = None

class ExperimentData(BaseModel):
    participantInfo: ParticipantInfo
    trialData: List[TrialData]

@app.post("/submit_data")
async def submit_data(data: ExperimentData):
    try:
        print(data)
        result = await collection.insert_one(data.dict())
        return {"message": "Data submitted successfully", "id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while submitting data: {str(e)}")

@app.get("/")
async def root():
    return {"message": "Experiment API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)