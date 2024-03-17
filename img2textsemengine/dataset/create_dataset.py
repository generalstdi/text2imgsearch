import json
from tqdm import tqdm
from datasets import load_dataset


def sample_coco_dataset(hf_card: str,
                        limit: int,
                        sample_path) -> None:
    """

    :param hf_card:
    :param limit:
    :param sample_path:
    :return:
    """
    dataset = load_dataset(hf_card, streaming=True, split="val")
    with open(sample_path, "w") as sample_file:
        for index, record in tqdm(enumerate(dataset), total=limit):
            if index <= limit:
                record.pop("image", None)
                sample_file.write(json.dumps(record) + "\n")
            else:
                break
