"""Add initial migration

Revision ID: 7e09fa75df7a
Revises: 
Create Date: 2021-09-28 22:19:53.415790

"""
import uuid
from hashlib import md5
from alembic import op
import sqlalchemy as sa
from app.deps.users import get_user_manager
import fastapi_users_db_sqlalchemy


# revision identifiers, used by Alembic.
revision = "7e09fa75df7a"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    users_table = op.create_table(
        "users",
        sa.Column("id", fastapi_users_db_sqlalchemy.GUID(), nullable=False),
        sa.Column("email", sa.String(length=320), nullable=False),
        sa.Column("hashed_password", sa.String(length=72), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("is_superuser", sa.Boolean(), nullable=False),
        sa.Column("is_verified", sa.Boolean(), nullable=False),
        sa.Column(
            "created",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column(
            "updated",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.bulk_insert(
        users_table,
        [
            {
                "id": str(uuid.uuid4()),
                "email": "admin@example.com",
                "hashed_password": next(get_user_manager()).password_helper.hash("Password123!"),
                "is_active": True,
                "is_superuser": True,
                "is_verified": True,
            },
            {
                "id": str(uuid.uuid4()),
                "email": f"user1@{str(uuid.uuid4())}.com",
                "hashed_password": next(get_user_manager()).password_helper.hash("Password123!"),
                "is_active": True,
                "is_superuser": True,
                "is_verified": True,
            },
            {
                "id": str(uuid.uuid4()),
                "email": "user2@facebook.com",
                "hashed_password": next(get_user_manager()).password_helper.hash("Password123!"),
                "is_active": True,
                "is_superuser": True,
                "is_verified": True,
            },
            {
                "id": str(uuid.uuid4()),
                "email": f"user3@{str(uuid.uuid4())}.com",
                "hashed_password": next(get_user_manager()).password_helper.hash("Password123!"),
                "is_active": True,
                "is_superuser": True,
                "is_verified": True,
            },
            {
                "id": str(uuid.uuid4()),
                "email": "user4@yahoo.com",
                "hashed_password": next(get_user_manager()).password_helper.hash("Password123!"),
                "is_active": True,
                "is_superuser": True,
                "is_verified": True,
            },
            {
                "id": str(uuid.uuid4()),
                "email": f"user5@{str(uuid.uuid4())}.com",
                "hashed_password": next(get_user_manager()).password_helper.hash("Password123!"),
                "is_active": True,
                "is_superuser": True,
                "is_verified": True,
            },
            {
                "id": str(uuid.uuid4()),
                "email": "user6@google.com",
                "hashed_password": next(get_user_manager()).password_helper.hash("Password123!"),
                "is_active": True,
                "is_superuser": True,
                "is_verified": True,
            },
        ]
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_table("users")
    # ### end Alembic commands ###
