from typing import ClassVar

from pydantic import BaseModel
from backend.database_models import User as DBUser, Group as DBGroup


class Meta(BaseModel):
    resourceType: str
    created: str
    lastModified: str

class GroupMeta(BaseModel):
    resourceType: str

class Name(BaseModel):
    givenName: str
    familyName: str


class BaseUser(BaseModel):
    userName: str
    name: Name
    active: bool

    schemas: list[str]


class BaseGroup(BaseModel):
    schemas: list[str]
    members: list[str]
    displayName: str


class CreateGroup(BaseGroup):
    pass


class CreateUser(BaseGroup):
    externalId: str


class UpdateUser(BaseUser):
    pass


class Operation(BaseModel):
    op: str
    value: dict[str, bool]


class PatchUser(BaseModel):
    schemas: list[str]
    Operations: list[Operation]


class Group(BaseGroup):
    @staticmethod
    def from_db_group(db_group: DBGroup) -> "Group":
        return Group(
            id=db_group.id,
            displayName=db_group.display_name,
            members=db_group.members,
            meta=GroupMeta(
                resourceType="Group",
            ),
            schemas=["urn:ietf:params:scim:schemas:core:2.0:Group"],
        )


class User(BaseUser):
    id: str
    externalId: str
    meta: Meta

    @staticmethod
    def from_db_user(db_user: DBUser) -> "User":
        given_name, family_name = db_user.fullname.split(" ")
        return User(
            id=db_user.id,
            userName=db_user.user_name,
            name=Name(givenName=given_name, familyName=family_name),
            active=db_user.active,
            externalId=db_user.external_id,
            meta=Meta(
                resourceType="User",
                created=db_user.created_at.isoformat(),
                lastModified=db_user.updated_at.isoformat(),
            ),
            schemas=["urn:ietf:params:scim:schemas:core:2.0:User"],
        )


class ListUserResponse(BaseModel):
    schemas: ClassVar[list[str]] = [
        "urn:ietf:params:scim:api:messages:2.0:ListResponse"
    ]
    totalResults: int
    startIndex: int
    itemsPerPage: int
    Resources: list[User]
