from pydantic import BaseModel


class LoginInfo(BaseModel):
    tenant_id: str
    """Tenant ID to login to"""

    subscription_id: str
    """Subscription ID to login to"""

    user_id: str
    """The app id of the user to login as"""

    user_key: str
    """The login key for the given user"""
