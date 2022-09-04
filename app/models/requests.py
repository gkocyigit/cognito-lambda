from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class CreateAccountRequest(BaseModel):
    username: str
    password: str
    image_id: Optional[str]
    is_recurring: bool = False
    date_created: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    email_verified_at: Optional[str]
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
    delete_flag: bool = False
    last_logged_in: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    last_modified: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    bvn:  Optional[str]
    pin:  Optional[str]
    question_1: Optional[str]
    question_2: Optional[str]
    question_3: Optional[str]
    answer_1: Optional[str]
    answer_2: Optional[str]
    answer_3: Optional[str]
    docType: Optional[str]
    last_login: str=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    date_joined: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    is_superuser: bool = False
    is_staff : bool = False
    is_active : bool = False
    countryCode: Optional[str]
    receive_notifications : bool = True
    date_of_birth: Optional[str]