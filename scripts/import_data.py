import os
from img2textsemengine.vector_db.qdrant_util import Importer
from img2textsemengine.utils.config import load_configurations

if __name__ == '__main__':
    configs = load_configurations("config/data/import.yaml")
    data_path = os.path.join(configs.data.dataset_folder, configs.data.dataset_file)
    importer = Importer(host=configs.qdrant.host,
                        port=configs.qdrant.port,
                        collection_name=configs.qdrant.collection_name,
                        image_vector_size=configs.vectors.image_vector_size,
                        hf_model=configs.hf_model,
                        dataset_path=data_path.__str__())  # to avoid expect type warnings
    importer.import_data(caption_payload_name=configs.qdrant.caption_payload_name)
