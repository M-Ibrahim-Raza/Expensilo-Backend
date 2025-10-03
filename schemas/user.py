from typing import Optional, Any
from typing_extensions import Annotated
from pydantic import BaseModel, EmailStr, Field, Json, ConfigDict


class UserBase(BaseModel):
    name: Annotated[
        str,
        Field(
            title="Full Name",
            description="The full name of the user",
            example="Alice Example",
        ),
    ]
    email: Annotated[
        EmailStr,
        Field(
            title="Email Address",
            description="Unique email address of the user",
            example="alice@example.com",
        ),
    ]
    password: Annotated[
        Optional[str],
        Field(
            title="Password",
            description="User's password (only required for local authentication)",
            example="password123",
            default=None,
        ),
    ]
    google_auth: Annotated[
        Optional[str],
        Field(
            title="Google Auth Token",
            description="OAuth2 token for Google authentication",
            example="ya29.A0AVA9y1...",
            default=None,
        ),
    ]
    preferences: Annotated[
        Json,
        Field(
            title="User Preferences",
            description="Preferences stored as JSON string",
            example='{"theme": "dark", "notifications": true}',
            default=None,
        ),
    ]


class UserCreate(UserBase):
    """Schema for creating a new user"""

    pass


class UserUpdate(BaseModel):
    """Schema for updating user fields"""

    name: Annotated[
        Optional[str],
        Field(
            title="Full Name",
            description="The full name of the user",
            example="Alice Updated",
            default=None,
        ),
    ] = None
    password: Annotated[
        Optional[str],
        Field(
            title="Password",
            description="New password to update",
            example="new_hashed_password_string",
            default=None,
        ),
    ] = None
    google_auth: Annotated[
        Optional[str],
        Field(
            title="Google Auth Token",
            description="Updated OAuth2 token for Google authentication",
            example="ya29.A0AVA9y2...",
            default=None,
        ),
    ] = None
    preferences: Annotated[
        Optional[str],
        Field(
            title="User Preferences",
            description="Updated preferences stored as JSON string",
            example='{"theme": "light", "notifications": false}',
            default=None,
        ),
    ] = None


# ---------- Read (Response) ----------
class UserRead(UserBase):
    """Schema for returning user details"""

    id: Annotated[
        int,
        Field(
            title="User ID",
            description="Unique identifier for the user",
            example=1,
        ),
    ]

    model_config = ConfigDict(from_attributes=True)
