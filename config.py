import os

from dotenv import load_dotenv


load_dotenv()


class Settings:

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    OPENAI_MODEL = os.getenv(
        "OPENAI_MODEL",
        "gpt-5.6-luna"
    )

    ENVIRONMENT = os.getenv(
        "ENVIRONMENT",
        "development"
    )


settings = Settings()