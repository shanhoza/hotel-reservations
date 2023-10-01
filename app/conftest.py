import os

# from unittest import mock

os.environ["MODE"] = "TEST"

# @cache from fastapi_cache can't be loaded while using pytest
# mock.patch("fastapi_cache.decorator.cache", lambda *args, **kwargs: lambda f: f).start()
