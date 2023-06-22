import importlib

from huggingface_hub import scan_cache_dir
from transformers import AutoConfig


def format_size(num: int) -> str:
    """Format size in bytes into a human-readable string.

    Taken from https://stackoverflow.com/a/1094933
    """
    num_f = float(num)
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if abs(num_f) < 1000.0:
            return f"{num_f:3.1f}{unit}"
        num_f /= 1000.0
    return f"{num_f:.1f}Y"


class HuggingFaceModelClass:
    """
    to search HuggingFaceModel information
    """
    def __init__(self):
        super(HuggingFaceModelClass, self).__init__()

    def getModels(self, certain_models=None):
        models = [{"id": i.repo_id, "size_on_disk": i.size_on_disk, "size_on_disk_str": i.size_on_disk_str}
                    for i in scan_cache_dir().repos]
        if certain_models is None:
            return models
        else:
            return list(filter(lambda x: x['id'] in certain_models, models)) if len(
                certain_models) > 0 else certain_models

    def getModelsSize(self, certain_models=None):
        models_size = scan_cache_dir().size_on_disk_str
        if certain_models is None:
            return models_size
        else:
            certain_models_size = sum(list(map(lambda x: x['size_on_disk'], self.getModels(certain_models))))
            return format_size(certain_models_size)

    def installHuggingFaceModel(self, model_name):
        try:
            config = AutoConfig.from_pretrained(model_name)

            class_name = config.architectures[0]

            # Import the module dynamically
            module = importlib.import_module('transformers')

            # Retrieve the class object from the module
            model_class = getattr(module, class_name)

            model_class.from_pretrained(model_name)

            return [obj for obj in self.getModels() if obj['id'] == model_name]
        except Exception as e:
            raise Exception(e)

    def removeHuggingFaceModel(self, model_name: str) -> str:
        try:
            commit_hashes = []
            cache_dir_result = scan_cache_dir()
            for i in cache_dir_result.repos:
                if model_name == i.repo_id:
                    for j in i.revisions:
                        commit_hashes.append(j.commit_hash)
            delete_strategy = cache_dir_result.delete_revisions(*commit_hashes)
            print("Will free " + delete_strategy.expected_freed_size_str)
            delete_strategy.execute()
            return model_name
        except Exception as e:
            print(e)
            return ''