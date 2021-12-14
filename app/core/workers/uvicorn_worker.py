from uvicorn.workers import UvicornWorker


class AppUvicornWorker(UvicornWorker):
    CONFIG_KWARGS = {
        **UvicornWorker.CONFIG_KWARGS,
        "server_header": False
    }
