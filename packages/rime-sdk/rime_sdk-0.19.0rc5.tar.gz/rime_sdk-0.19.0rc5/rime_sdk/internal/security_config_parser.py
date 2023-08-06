"""Parse protos / configs for the RIME file scanning service."""
from rime_sdk.protos.schema.file_scanning.file_scanning_config_pb2 import (
    HuggingfaceModelInfo,
    ModelFileInfo,
    PytorchModelInfo,
)


def convert_model_info_to_dict(model_file_info: ModelFileInfo) -> dict:
    """Convert a model info dict to a proto."""
    which_file_info = model_file_info.WhichOneof("file_info")
    if which_file_info == "pytorch_file":
        return {
            "scan_type": "pytorch",
            "scan_path": model_file_info.pytorch_file.scan_path,
        }
    elif which_file_info == "huggingface_file":
        return {
            "scan_type": "huggingface",
            "scan_path": model_file_info.huggingface_file.scan_path,
        }
    else:
        raise ValueError(f"Unknown file info type: {which_file_info}")


def model_info_from_dict(model_info_dict: dict) -> ModelFileInfo:
    """Convert a model info dict to a proto."""
    scan_type = model_info_dict.get("scan_type")
    if scan_type is None:
        raise ValueError("The model_file_info must specify a scan type")
    scan_path = model_info_dict.get("scan_path")
    if scan_path is None:
        raise ValueError("The model_file_info must specify a scan path")
    proto_config = ModelFileInfo()
    if scan_type == "huggingface":
        hf_model_info = HuggingfaceModelInfo(scan_path=scan_path)
        proto_config.huggingface_file.CopyFrom(hf_model_info)
    elif scan_type == "pytorch":
        pytorch_model_info = PytorchModelInfo(scan_path=scan_path)
        proto_config.pytorch_file.CopyFrom(pytorch_model_info)
    else:
        raise ValueError(f"Invalid scan type {scan_type}")
    return proto_config
