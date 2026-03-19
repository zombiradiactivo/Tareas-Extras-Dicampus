import pytest
from src_refactorizar.database import db_handler


@pytest.fixture(autouse=True)
def temporary_database(tmp_path, monkeypatch):
    """Configura una base de datos SQLite temporal para cada test."""
    path = tmp_path / "test_video_club.db"
    monkeypatch.setattr(db_handler, "DB_PATH", str(path))
    db_handler.create_tables()
    return str(path)
