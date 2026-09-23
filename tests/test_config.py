from config import settings


def test_openai_model():
    assert settings.OPENAI_MODEL == "gpt-5.6-luna"


def test_environment():
    assert settings.ENVIRONMENT == "development"