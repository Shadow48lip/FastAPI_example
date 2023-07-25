import sqlalchemy as sa
import sqlalchemy.orm as so

from src.conf.database import Base

"""
CREATE TABLE users (
    id INT(11) NOT NULL AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    age INT(11) NOT NULL,
    PRIMARY KEY (id)
);
"""


class User(Base):
    __tablename__ = "users"

    id: so.Mapped[int] = so.mapped_column(primary_key=True, nullable=False, autoincrement=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(100))
    age: so.Mapped[int]
