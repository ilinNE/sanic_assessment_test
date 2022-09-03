TORTOISE_ORM = {
    "connections": {"default": "postgres://dev_user:123456@localhost:5432/dev_db"},
    "apps": {
        "models": {
            "models": ["app.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}

SECRET = "12312321312"