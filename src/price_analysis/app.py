from fastapi import FastAPI


def create_app() -> FastAPI:
    """
    Роуты и обработчики всего приложения
    :return: app
    """
    app = FastAPI(
        title = "Анализ цен",
        version = "1.0.0",
        description = "Динамическое ценообразование и анализ конкурентов"
    )

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    return app

app = create_app()