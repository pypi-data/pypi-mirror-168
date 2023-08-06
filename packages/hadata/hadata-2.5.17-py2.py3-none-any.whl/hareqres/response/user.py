from pydantic import BaseModel


class UserProfileResponse(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: str
    organization_id: str
    profile_type: str
    is_verified: bool
