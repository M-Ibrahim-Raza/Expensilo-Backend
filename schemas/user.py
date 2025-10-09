from typing import Optional, Any

from typing_extensions import Annotated
from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserCreateRequest(BaseModel):

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
            title="Hashed Password",
            description="User's new hashed password",
            example="$2b$12$uH1cE5tHhH7oQk1DjOQx",
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
        dict[str, Any] | None,
        Field(
            title="User Preferences",
            description="Preferences stored as JSON",
            example={"theme": "dark", "notifications": True},
            default=None,
        ),
    ]


class UserResponse(BaseModel):

    id: Annotated[
        int,
        Field(
            title="User ID",
            description="Unique identifier for the user",
            example=1,
        ),
    ]

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

    hashed_password: Annotated[
        Optional[str],
        Field(
            title="Hashed Password",
            description="User's hashed password",
            example="$2b$12$uH1cE5tHhH7oQk1DjOQx",
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
        dict[str, Any] | None,
        Field(
            title="User Preferences",
            description="Preferences stored as JSON",
            example={"theme": "dark", "notifications": True},
            default=None,
        ),
    ]

    model_config = ConfigDict(from_attributes=True)


class UserUpdateRequest(BaseModel):

    name: Annotated[
        Optional[str],
        Field(
            title="Full Name",
            description="The full name of the user",
            example="Alice Updated",
            default=None,
        ),
    ]
    password: Annotated[
        Optional[str],
        Field(
            title="Hashed Password",
            description="User's new hashed password",
            example="$2b$12$uH1cE5tHhH7oQk1DjOQx",
            default=None,
        ),
    ]
    google_auth: Annotated[
        Optional[str],
        Field(
            title="Google Auth Token",
            description="Updated OAuth2 token for Google authentication",
            example="ya29.A0AVA9y2...",
            default=None,
        ),
    ]
    preferences: Annotated[
        dict[str, Any] | None,
        Field(
            title="User Preferences",
            description="Updated preferences stored as JSON string",
            example='{"theme": "light", "notifications": false}',
            default=None,
        ),
    ]
