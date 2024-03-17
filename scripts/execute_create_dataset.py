from img2textsemengine.dataset.create_dataset import sample_coco_dataset

if __name__ == '__main__':
    sample_coco_dataset(hf_card="lmms-lab/COCO-Caption",
                        limit=100,
                        sample_path="dataset/sample.jsonl")
