from pydantic import BaseModel
from typing import Optional, List

class SoilInput(BaseModel):
    nitrogen: float
    phosphorus: float
    potassium: float
    ph: float
    district: Optional[str] = 'Thanjavur'
    land_acres: Optional[float] = 2.0

class SellDecisionInput(BaseModel):
    crop: str
    current_price: float
    monthly_storage_cost: float = 35.0
    annual_interest_rate: float = 7.0
    holding_months: int = 2

class BestMarketInput(BaseModel):
    crop: str
    current_district: str
    quantity_quintals: float = 50.0
    transport_rate_per_km_quintal: float = 1.5

class FeedbackInput(BaseModel):
    recommendation_type: str
    useful: bool
    comment: Optional[str] = None
