TORTOISE_ORM = {
    "connections": {"default": "postgres://dev_user:123456@localhost:5432/dev_db"},
    "apps": {
        "models": {
            "models": ["models", "aerich.models"],
            "default_connection": "default",
        },
    },
}