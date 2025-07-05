from pydantic import BaseModel, Field
from typing import List, Optional

class PersonalInformation(BaseModel):
    last_name: str = Field(..., description="Patient's last name")
    first_name: str = Field(..., description="Patient's first name")
    date_of_birth: Optional[str] = Field(None, description="Patient's date of birth")

class Surgery(BaseModel):
    name: Optional[str] = Field(None, description="Name of the surgery")
    year: Optional[int] = Field(None, description="Year the surgery was performed")

class MedicalHistory(BaseModel):
    conditions: Optional[List[str]] = Field(None, description="List of medical conditions")
    surgeries: Optional[List[Surgery]] = Field(None, description="List of surgeries")

class Allergy(BaseModel):
    substance: Optional[str] = Field(None, description="Substance the patient is allergic to")
    reaction: Optional[str] = Field(None, description="Reaction to the substance")

class Treatment(BaseModel):
    medication: Optional[str] = Field(None, description="Name of the medication")
    dosage: Optional[str] = Field(None, description="Dosage of the medication")
    schedule: Optional[str] = Field(None, description="Schedule for taking the medication")

class Lifestyle(BaseModel):
    relationship_status: Optional[str] = Field(None, description="Patient's relationship status")
    children: Optional[bool] = Field(None, description="Whether the patient has children")
    living_alone: Optional[bool] = Field(None, description="Whether the patient lives alone")
    alcohol_tobacco_use: Optional[str] = Field(None, description="Patient's alcohol and tobacco use")

class LabResult(BaseModel):
    date: Optional[str] = Field(None, description="Date of the lab result")
    sodium_mmol_per_L: Optional[int] = Field(None, description="Sodium level in mmol/L")
    potassium_mmol_per_L: Optional[float] = Field(None, description="Potassium level in mmol/L")
    creatinine_umol_per_L: Optional[int] = Field(None, description="Creatinine level in umol/L")

class Imaging(BaseModel):
    date: Optional[str] = Field(None, description="Date of the imaging")
    type: Optional[str] = Field(None, description="Type of imaging")
    result: Optional[str] = Field(None, description="Result of the imaging")

class PatientRecord(BaseModel):
    personal_information: Optional[PersonalInformation] = Field(None, description="Patient's personal information")
    medical_history: Optional[MedicalHistory] = Field(None, description="Patient's medical history")
    allergies: Optional[List[Allergy]] = Field(None, description="List of patient's allergies")
    treatment: Optional[List[Treatment]] = Field(None, description="List of patient's treatments")
    lifestyle: Optional[Lifestyle] = Field(None, description="Patient's lifestyle information")
    lab_results: Optional[List[LabResult]] = Field(None, description="List of patient's lab results")
    imaging: Optional[List[Imaging]] = Field(None, description="List of patient's imaging results")
