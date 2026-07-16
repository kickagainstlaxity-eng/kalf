import os

class Config:
    SECRET_KEY = os.environ.get(
        "FLASK_SECRET_KEY",
        "kalf_fallback_secret_key_2026"
    )

    PAYSTACK_SECRET_KEY = os.environ.get(
        "PAYSTACK_SECRET_KEY",
        "sk_test..."
    )

    TEMPLATES_AUTO_RELOAD = True