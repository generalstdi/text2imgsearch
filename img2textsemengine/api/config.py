import yaml
from os.path import expandvars
from pydantic import BaseModel


class QdrantParams(BaseModel):
    """
    A class to store the qdrant parameters
    """
    host: str
    port: int
    collection_name: str


class Model(BaseModel):
    """
    A class to define the HF model will be used to extract the embeddings of texts/images
    """
    hf_model: str


class VectorNames(BaseModel):
    """
    A class to define the DB columns that stores the image/text vectors
    """
    text_vector_name: str
    img_vector_name: str


class Config(BaseModel):
    """
    A class that stores the configs of the Searcher class
    """
    qdrant: QdrantParams
    vector_names: VectorNames
    model: Model


def load_config(path: str) -> Config:
    """Loads configurations"""
    with open(path, "r", encoding='utf-8') as stream:
        config = yaml.load(expandvars(stream.read()), Loader=yaml.FullLoader)
        config = Config(**config)
    return config
