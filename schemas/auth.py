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


# class LoginRequest(BaseModel):

#     email: Annotated[
#         EmailStr,
#         Field(
#             ...,
#             title="Email Address",
#             description="Unique email address of the user",
#             example="alice@example.com",
#         ),
#     ]

#     password: Annotated[
#         str,
#         Field(
#             ...,
#             title="Password",
#             description="User's password (only required for local authentication)",
#             example="password123",
#         ),
#     ]


class Token(BaseModel):

    access_token: Annotated[
        str,
        Field(
            ...,
            title="Access Token",
            description="JWT access token used to authorize requests to protected endpoints",
            example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        ),
    ]
    token_type: Annotated[
        str,
        Field(
            ...,
            title="Token Type",
            description="Type of the token, usually 'bearer'",
            example="bearer",
        ),
    ]
