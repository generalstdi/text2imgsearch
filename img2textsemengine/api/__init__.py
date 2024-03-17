from contextlib import asynccontextmanager
import os
from fastapi import FastAPI
from img2textsemengine.api.config import load_config
from img2textsemengine.vector_db.qdrant_util import Searcher


searchers = {}


@asynccontextmanager
async def lifespan(fastapi_app: FastAPI) -> None:
    """
    Load all the global variables here
    :param fastapi_app: the fastAPI application to startup. Not used, however, if we delete it we will receive
    an error message like 'application startup failed. Exiting'
    """
    configs = load_config(path=os.environ.get("config_file", "config/api/api_configs.yaml"))  # it can be defined as an
    # env variable. If there is not such an env var, then use the default config file
    searcher = Searcher(host=configs.qdrant.host,
                        port=configs.qdrant.port,
                        collection_name=configs.qdrant.collection_name,
                        text_vector_name=configs.vector_names.text_vector_name,
                        img_vector_name=configs.vector_names.img_vector_name,
                        hf_model=configs.model.hf_model)
    searchers["base_searcher"] = searcher
    yield
    searchers.clear()
