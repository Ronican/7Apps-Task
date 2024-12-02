# tests/test_app_import.py


def test_import_app():
    from app.main import app

    assert app is not None
