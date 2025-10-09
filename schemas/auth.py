from typing_extensions import Annotated
from pydantic import BaseModel, EmailStr, Field


class SignUpRequest(BaseModel):

    name: Annotated[
        str,
        Field(
            ...,
            title="Full Name",
            description="The full name of the user",
            example="Alice Example",
        ),
    ]

    email: Annotated[
        EmailStr,
        Field(
            ...,
            title="Email Address",
            description="Unique email address of the user",
            example="alice@example.com",
        ),
    ]

    password: Annotated[
        str,
        Field(
            ...,
            title="Password",
            description="User's password (only required for local authentication)",
            example="password123",
        ),
    ]
