from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime

messy_data = {
  "user_id": "94820", 
  "signup_date": "2026-06-01T18:00:00Z",
  "is_premium": "True",
  "account_balance": "150.75",
  "phone_number": None,
  "referred_by": "   "
}

class Parse(BaseModel):
    user_id: int
    signup_date: datetime
    is_premium: bool
    account_balance: float
    phone_number: Optional[str] = None
    referred_by: Optional[str] = None
    
    @field_validator('referred_by', mode='before')
    @classmethod
    def validate_referred_by(cls, value:str) -> Optional[str]:
        if value and isinstance(value, str):
            cleaned = value.strip()
            if not cleaned:
                return None
            return cleaned
        return value
        
parse = Parse(**messy_data)
print(parse.model_dump())
