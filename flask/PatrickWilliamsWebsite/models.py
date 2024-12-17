from datetime import datetime, timezone
import sqlalchemy as sa
import sqlalchemy.orm as so
from . import db

class Bees(db.Model):
    __tablename__= 'bees'
    id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True, nullable=True)
    print_date: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc), nullable=True)
    letters: so.Mapped[str] = so.mapped_column(sa.String(7), nullable=False)
    accepted: so.Mapped[str] = so.mapped_column(sa.Text(), nullable=False)
    pangrams: so.Mapped[str] = so.mapped_column(sa.Text(), nullable=True)

class Boxes(db.Model):
    __tablename__= 'boxes'
    id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True, nullable=True)
    print_date: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc), nullable=True)
    sides: so.Mapped[str] = so.mapped_column(sa.Text(), nullable=False)
    dictionary: so.Mapped[str] = so.mapped_column(sa.Text(), nullable=False)
    one_word: so.Mapped[str] = so.mapped_column(sa.Text(), nullable=True)
    two_word: so.Mapped[str] = so.mapped_column(sa.Text(), nullable=True)
