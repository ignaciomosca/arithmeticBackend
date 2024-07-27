"""empty message

Revision ID: 9937e0baf906
Revises: 9f9b1e3981fe
Create Date: 2024-07-27 10:29:10.029537

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "9937e0baf906"
down_revision = "9f9b1e3981fe"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(
        "fk_records_operations", "records", "operations", ["operation_id"], ["id"]
    )
    op.create_foreign_key("fk_records_users", "records", "users", ["user_id"], ["id"])
    op.execute("INSERT INTO operations (type, cost) VALUES ('ADDITION', 1)")
    op.execute("INSERT INTO operations (type, cost) VALUES ('SUBTRACTION', 1)")
    op.execute("INSERT INTO operations (type, cost) VALUES ('MULTIPLICATION', 1)")
    op.execute("INSERT INTO operations (type, cost) VALUES ('DIVISION', 1)")
    op.execute("INSERT INTO operations (type, cost) VALUES ('SQUARE', 5)")
    op.execute("INSERT INTO operations (type, cost) VALUES ('RANDOM', 10)")

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("fk_records_operations", "records", type_="foreignkey")
    op.drop_constraint("fk_records_users", "records", type_="foreignkey")
    op.execute("TRUNCATE TABLE operations")
    # ### end Alembic commands ###
