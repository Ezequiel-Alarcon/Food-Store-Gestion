"""Database package: migrations and seed data."""
from app.db.seed import run_seed

__all__ = ["run_seed"]