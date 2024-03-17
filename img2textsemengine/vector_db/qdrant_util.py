import requests
import torch
from tqdm import tqdm
from datasets import load_dataset
from PIL import Image
from qdrant_client import QdrantClient
from qdrant_client.http import models
from transformers import AutoTokenizer, CLIPModel, AutoProcessor


class Importer(object):
    """
    A class to import the data in QDrant
    """
    def __init__(self,
                 host: str,
                 port: int,
                 collection_name: str,
                 image_vector_size: int,
                 hf_model: str,
                 dataset_path: str):
        """
        Initialize the importer class. Expecially, we establish the qdrant client
        and initializing the clip model that will be used to extract
        the embeddings of the images
        :param host: qdrant host
        :param port: qdrant port
        :param collection_name: the collection to store the metadata
        :param image_vector_size: the size of the image vector
        :param hf_model: the model which is responsible for extracting the embeddings of the images/texts
        :param dataset_path: the path of the input dataset
        """

        self.qdrant_client = QdrantClient(location=host, port=port)
        self.collection_name = collection_name
        self.__init_qdrant_collection(image_vector_size=image_vector_size)
        # Initialize huggingface's model and processor
        self.tokenizer = AutoTokenizer.from_pretrained(hf_model)
        self.model = CLIPModel.from_pretrained(hf_model)
        self.processor = AutoProcessor.from_pretrained(hf_model)
        self.dataset = load_dataset("json", data_files=dataset_path)["train"]

    def __init_qdrant_collection(self, image_vector_size: int) -> None:
        """
        Initialize the collection and specifying the vector(s) parameters
        :param image_vector_size: the size of the image vector
        :return: None
        """
        vectors_config = {
            "text": models.VectorParams(
                size=512,
                distance=models.Distance.COSINE,
            ),
            "image": models.VectorParams(
                size=512,
                distance=models.Distance.COSINE,
            ),
        }
        self.qdrant_client.recreate_collection(
            collection_name=self.collection_name,
            vectors_config=vectors_config)

    def import_data(self, caption_payload_name) -> None:
        """
        Populate the QDrant DB with the metadata of the dataset. In detail, we will use as
        'id' the index of the corresponding record in the dataset. As vector will be stored the
        clip embedding of the image. As payload will be stored the answers provided by the coc dataset. They will be used to evaluate the accuracy of our system.
        :return: None
        """
        total_size = len(self.dataset)
        for index, record in tqdm(enumerate(self.dataset), total=total_size):
            url = record["coco_url"]

            image_features = self.__extract_image_emb(img_url=url)
            text_features = self.__extract_text_emb(answers=record["answer"])
            point = models.PointStruct(id=index,
                                       vector={
                                           "image": image_features[0].tolist(),
                                           "text": text_features.tolist()
                                       },
                                       payload={
                                           caption_payload_name: record["answer"],
                                           "img_url": url
                                       })
            self.qdrant_client.upsert(collection_name=self.collection_name, points=[point])

    def __extract_image_emb(self, img_url: str) -> torch.Tensor:
        """
        extract the embedding of an image
        :param img_url: the url of the image
        :return a tensor representing the image embedding
        """
        image = Image.open(requests.get(img_url, stream=True).raw)
        inputs = self.processor(images=image, return_tensors="pt")
        image_features = self.model.get_image_features(**inputs)
        return image_features

    def __extract_text_emb(self, answers: str) -> torch.Tensor:
        """
        extract the text embedding of each provided caption/answer for a given image. Then return as
        the text embedding of the image the average embedding of the extracted of each caption/answer
        :param answers: the captions/answers of the image
        :return the avg/mean embedding of all the captions
        """
        inputs = self.tokenizer(answers,
                                padding=True,
                                return_tensors="pt")
        text_features = self.model.get_text_features(**inputs)
        return torch.mean(text_features, dim=0)


class Searcher(object):
    """
    A class to implement any functionality regarding searching in the QDrant DB
    """
    def __init__(self,
                 host: str,
                 port: int,
                 collection_name: str,
                 text_vector_name: str,
                 img_vector_name: str,
                 hf_model: str):
        """
        Initializa the qdrant client and all the objects for the clip model. Also, define the name of the
        vector names to be queried to retrieve the top-k candidates
        :param host: the QDrant host
        :param port: the port of the QDrant
        :param collection_name: the collection to query
        :param text_vector_name: the name of the column where the text vector is stored
        :param img_vector_name: the name of the image vector column where the image vector is stored
        :param hf_model: the huggingface model to extract the embedding of the text query
        """
        self.qdrant_client = QdrantClient(location=host, port=port)
        self.collection_name = collection_name
        self.tokenizer = AutoTokenizer.from_pretrained(hf_model)
        self.model = CLIPModel.from_pretrained(hf_model)
        self.text_vector_name = text_vector_name
        self.img_vector_name = img_vector_name
        self.possible_vector_names = [text_vector_name, img_vector_name]

    def query(self,
              text: str,
              vector_to_search: str,
              top_k: int = 10) -> list[tuple[str, list[str]]]:
        """
        given a text query retrieve the top-k candidates. Based on the vector_to_search parameter, it will retrieve the
        top-k candidates based on the mentioned vector. It could be either "image" or "text".
        :param text: the user query
        :param vector_to_search: the vector column to use in order to retrieve the top-k candidates for the user query
        :param top_k: the number of retrieved results
        :return a list with the top-k results. Each instance will be a tuple where the first element will be the img url
        and the second one will be a list with the captions/answers of the image
        """
        if vector_to_search not in self.possible_vector_names:
            raise ValueError(f"'vector_to_search' parameter must be either {self.text_vector_name} or "
                             f"{self.img_vector_name}")
        inputs = self.tokenizer([text], padding=True, return_tensors="pt")
        text_features = self.model.get_text_features(**inputs).tolist()[0]
        response = self.qdrant_client.search(collection_name=self.collection_name,
                                             query_vector=models.NamedVector(
                                                 name=vector_to_search,
                                                 vector=text_features
                                             ),
                                             append_payload=True,
                                             limit=top_k)
        output = [(result.payload["img_url"], result.payload["possible_answers"]) for result in response]
        return output
