from typing import Optional
from pydantic import BaseModel

class AccountDetailResponse(BaseModel):
    first_name : Optional[str]
    last_name : Optional[str]
    fullname : Optional[str]
    phone_number: Optional[str]
    profile_type: Optional[str]
    balance: Optional[str]
    tenant_id: Optional[str]
    promo_code: Optional[str]
    formatted_date: Optional[str]
    account_number:  Optional[str]
    father_name: Optional[str]
    status: Optional[str]
    address: Optional[str]
    dob: Optional[str]
    city: Optional[str]
    gender: Optional[str]
    rating: Optional[str]
    state: Optional[str]
    country: Optional[str]
