"""Parse json config to proto."""
import copy
import json
from copy import deepcopy
from typing import Any, Dict, Optional, Tuple

from google.protobuf.message import Message

from rime_sdk.protos.result_synthesizer.result_message_pb2 import DataType
from rime_sdk.protos.schema.cli_config.cli_config_pb2 import (
    EmbeddingInfo,
    HuggingFaceSingleDataLoadingInfo,
    ImagesCLIConfig,
    ImagesDataInfo,
    ImagesSingleDataFileInfo,
    ImagesSingleDataInfo,
    NLPCLIConfig,
    NLPDataInfo,
    NLPIncrementalConfig,
    NLPSingleDataFileInfo,
    NLPSingleDataInfo,
    RankingInfo,
    SingleDataCollectorInfo,
    SingleDataLoadingInfo,
    SingleDeltaLakeInfo,
    SinglePredictionInfo,
    TabularCLIConfig,
    TabularDataInfo,
    TabularIncrementalConfig,
    TabularSingleDataFileInfo,
    TabularSingleDataInfo,
    TabularSingleDataInfoParams,
    TypedCLIConfig,
    TypedIncrementalConfig,
    UnstructuredEmbeddingInfo,
    UnstructuredSingleDataInfoParams,
)


def convert_tabular_params_to_proto(
    config: dict,
) -> Optional[TabularSingleDataInfoParams]:
    """Convert tabular params dictionary to proto."""
    proto_names = [
        field.name for field in TabularSingleDataInfoParams.DESCRIPTOR.fields
    ]
    param_config = {name: config.pop(name) for name in proto_names if name in config}
    if len(param_config) == 0:
        return None
    if "loading_kwargs" in param_config and param_config["loading_kwargs"] is not None:
        param_config["loading_kwargs"] = json.dumps(param_config["loading_kwargs"])
    if "ranking_info" in param_config and param_config["ranking_info"] is not None:
        param_config["ranking_info"] = RankingInfo(**param_config["ranking_info"])
    if "embeddings" in param_config and param_config["embeddings"] is not None:
        param_config["embeddings"] = [
            EmbeddingInfo(**info) for info in param_config["embeddings"]
        ]
    return TabularSingleDataInfoParams(**param_config)


def convert_single_tabular_data_info_to_proto(config: dict) -> TabularSingleDataInfo:
    """Convert a dictionary to single tabular data info proto message."""
    tabular_params = convert_tabular_params_to_proto(config)
    config_type = config.pop("type", "default")
    if config_type == "default":
        sample = config["sample"] if "sample" in config else None
        single_data_file_info_proto = TabularSingleDataFileInfo(
            file_name=config["file_name"], sample=sample
        )
        proto = TabularSingleDataInfo(
            single_params=tabular_params,
            single_data_file_info=single_data_file_info_proto,
        )
    elif config_type == "custom":
        loader_kwargs_json = ""
        if "loader_kwargs" in config and config["loader_kwargs"] is not None:
            loader_kwargs_json = json.dumps(config["loader_kwargs"])
        if "loader_kwargs_json" in config and config["loader_kwargs_json"] is not None:
            loader_kwargs_json = config["loader_kwargs_json"]
        single_data_loading_info_proto = SingleDataLoadingInfo(
            load_path=config["load_path"],
            load_func_name=config["load_func_name"],
            loader_kwargs_json=loader_kwargs_json,
        )
        proto = TabularSingleDataInfo(
            single_params=tabular_params,
            single_data_loading_info=single_data_loading_info_proto,
        )
    elif config_type == "data_collector":
        single_data_collector_info_proto = SingleDataCollectorInfo(
            start_time=config["start_time"], end_time=config["end_time"]
        )
        proto = TabularSingleDataInfo(
            single_params=tabular_params,
            single_data_collector_info=single_data_collector_info_proto,
        )
    elif config_type == "delta_lake":
        single_delta_lake_info_proto = SingleDeltaLakeInfo(
            server_hostname=config["server_hostname"],
            http_path=config["http_path"],
            table_name=config["table_name"],
            start_time=config["start_time"],
            end_time=config["end_time"],
            time_col=config["time_col"],
        )
        proto = TabularSingleDataInfo(
            single_params=tabular_params,
            single_delta_lake_info=single_delta_lake_info_proto,
        )
    else:
        raise ValueError(f"Unsupported config type: {config_type}")
    return proto


def convert_default_tabular_data_info_to_split(
    config: dict,
) -> Tuple[TabularSingleDataInfo, TabularSingleDataInfo]:
    """Convert default TabularDataInfo config to split ref and eval SingleDataInfo protos."""
    ref_config = {"file_name": config.pop("ref_path")}
    eval_config = {"file_name": config.pop("eval_path")}
    if "ref_pred_path" in config:
        ref_config["pred_path"] = config.pop("ref_pred_path")
    if "eval_pred_path" in config:
        eval_config["pred_path"] = config.pop("eval_pred_path")
    ref_config.update(config)
    eval_config.update(config)
    ref_data_info = convert_single_tabular_data_info_to_proto(ref_config)
    eval_data_info = convert_single_tabular_data_info_to_proto(eval_config)
    return ref_data_info, eval_data_info


def convert_tabular_data_info_to_proto(config: dict) -> TabularDataInfo:
    """Convert a dictionary to tabular data info proto message."""
    config_type = config.get("type", "default")

    if config_type == "default":
        ref_data_info, eval_data_info = convert_default_tabular_data_info_to_split(
            config
        )
    elif config_type == "custom":
        # TabularDataLoadingInfo
        eval_config = config.copy()
        config["load_func_name"] = "get_ref_data"
        ref_data_info = convert_single_tabular_data_info_to_proto(config)
        eval_config["load_func_name"] = "get_eval_data"
        eval_data_info = convert_single_tabular_data_info_to_proto(eval_config)
    elif config_type == "split":
        eval_data_info = convert_single_tabular_data_info_to_proto(
            config["eval_data_info"]
        )
        ref_data_info = convert_single_tabular_data_info_to_proto(
            config["ref_data_info"]
        )
    else:
        raise ValueError(f"Unsupported config type: {config['type']}")

    return TabularDataInfo(ref_data_info=ref_data_info, eval_data_info=eval_data_info)


def convert_tabular_config_to_proto(config: dict) -> TabularCLIConfig:
    """Convert config to tabular proto."""
    # pop to remove from original config dict
    data_info = convert_tabular_data_info_to_proto(config.pop("data_info"))
    proto = TabularCLIConfig(data_info=data_info)
    config_field_names = [field.name for field in TabularCLIConfig.DESCRIPTOR.fields]
    for name in config_field_names:
        if name in config and config[name] is not None:
            # pop to remove from original config dict
            setattr(proto, name, json.dumps(config.pop(name)))
    return proto


def convert_single_unstructured_params_to_proto(
    config: dict,
) -> Optional[UnstructuredSingleDataInfoParams]:
    """Convert unstructured params dictionary to proto."""
    result: Dict[str, Any] = {}
    if "prediction_info" in config and config["prediction_info"] is not None:
        single_pred_info = SinglePredictionInfo(**config["prediction_info"])
        result["prediction_info"] = single_pred_info
    if "embeddings" in config and config["embeddings"] is not None:
        embeddings = [
            UnstructuredEmbeddingInfo(**info) for info in config["embeddings"]
        ]
        result["embeddings"] = embeddings
    if len(result) == 0:
        return None
    else:
        return UnstructuredSingleDataInfoParams(**result)


def convert_single_nlp_data_info_to_proto(config: dict) -> NLPSingleDataInfo:
    """Convert a dictionary to single nlp data info proto message."""
    unstructured_params = convert_single_unstructured_params_to_proto(config)
    config_type = config.pop("type", "default")
    if config_type == "default":
        return NLPSingleDataInfo(
            single_data_file_info=NLPSingleDataFileInfo(file_name=config["file_name"]),
            single_params=unstructured_params,
        )
    elif config_type == "custom":
        loader_kwargs_json = ""
        if "loader_kwargs" in config and config["loader_kwargs"] is not None:
            loader_kwargs_json = json.dumps(config["loader_kwargs"])
        if "loader_kwargs_json" in config and config["loader_kwargs_json"] is not None:
            loader_kwargs_json = config["loader_kwargs_json"]
        single_data_loading_info = SingleDataLoadingInfo(
            load_path=config["load_path"],
            load_func_name=config["load_func_name"],
            loader_kwargs_json=loader_kwargs_json,
        )
        return NLPSingleDataInfo(
            single_data_loading_info=single_data_loading_info,
            single_params=unstructured_params,
        )
    elif config_type == "huggingface":
        huggingface_single_info = HuggingFaceSingleDataLoadingInfo(
            dataset_uri=config["dataset_uri"],
            split_name=config["split_name"],
            text_key=config["text_key"],
            loading_params_json=json.dumps(config["loading_params"]),
        )
        if "label_key" in config and config["label_key"] is not None:
            huggingface_single_info.label_key = config["label_key"]
        if "text_pair_key" in config and config["text_pair_key"] is not None:
            huggingface_single_info.text_pair_key = config["text_pair_key"]
        return NLPSingleDataInfo(
            huggingface_single_data_loading_info=huggingface_single_info,
            single_params=unstructured_params,
        )
    elif config_type == "delta_lake":
        single_delta_lake_info_proto = SingleDeltaLakeInfo(
            server_hostname=config["server_hostname"],
            http_path=config["http_path"],
            table_name=config["table_name"],
            start_time=config["start_time"],
            end_time=config["end_time"],
            time_col=config["time_col"],
        )
        return NLPSingleDataInfo(
            single_delta_lake_info=single_delta_lake_info_proto,
            single_params=unstructured_params,
        )
    elif config_type == "data_collector":
        single_data_collector_info_proto = SingleDataCollectorInfo(
            start_time=config["start_time"], end_time=config["end_time"]
        )
        if unstructured_params is not None and unstructured_params.HasField(
            "prediction_info"
        ):
            raise ValueError(
                "'prediction_info' cannot be specified with data config"
                f" of type {config_type}"
            )
        return NLPSingleDataInfo(
            single_data_collector_info=single_data_collector_info_proto,
            single_params=unstructured_params,
        )
    else:
        raise ValueError(f"Unsupported config type: {config_type}")


def _get_default_nlp_data_info_split_configs(config: dict) -> Tuple[dict, dict]:
    """Get default NLP config type data info split configs."""
    ref_config = {"file_name": config.pop("ref_path")}
    eval_config = {"file_name": config.pop("eval_path")}
    ref_config.update(config)
    eval_config.update(config)
    return ref_config, eval_config


def _get_custom_nlp_data_info_split_configs(config: dict) -> Tuple[dict, dict]:
    """Get custom NLP config type data info split configs."""
    ref_config = {"load_func_name": "get_ref_data"}
    eval_config = {"load_func_name": "get_eval_data"}
    ref_config.update(config)
    eval_config.update(config)
    return ref_config, eval_config


def _get_huggingface_data_info_split_configs(config: dict) -> Tuple[dict, dict]:
    """Get huggingface config type data info split configs."""
    ref_config, eval_config = {}, {}
    if "ref_split" in config:
        ref_config["split_name"] = config.pop("ref_split")
    if "eval_split" in config:
        eval_config["split_name"] = config.pop("eval_split")
    if "eval_label_key" in config:
        eval_config["label_key"] = config.pop("eval_label_key")
    ref_config.update(config)
    if "label_key" in config:
        del config["label_key"]
    eval_config.update(config)
    return ref_config, eval_config


def convert_nlp_data_info_to_proto(config: dict) -> NLPDataInfo:
    """Convert config to proto message for nlp data."""
    config_type = config.get("type", "default")
    if config_type == "default":
        ref_config, eval_config = _get_default_nlp_data_info_split_configs(config)
    elif config_type == "custom":
        ref_config, eval_config = _get_custom_nlp_data_info_split_configs(config)
    elif config_type == "huggingface":
        ref_config, eval_config = _get_huggingface_data_info_split_configs(config)
    elif config_type == "split":
        ref_config = config["ref_data_info"]
        eval_config = config["eval_data_info"]
    else:
        raise ValueError(f"Unsupported config type: {config['type']}")
    ref_data_info = convert_single_nlp_data_info_to_proto(ref_config)
    eval_data_info = convert_single_nlp_data_info_to_proto(eval_config)
    return NLPDataInfo(ref_data_info=ref_data_info, eval_data_info=eval_data_info)


def convert_nlp_config_to_proto(config: dict) -> NLPCLIConfig:
    """Convert config to nlp proto."""
    # pop to remove from original config dict
    data_info = convert_nlp_data_info_to_proto(config.pop("data_info"))
    proto = NLPCLIConfig(data_info=data_info)
    config_names = [field.name for field in NLPCLIConfig.DESCRIPTOR.fields]
    for name in config_names:
        if name in config and config[name] is not None:
            # pop to remove from original config dict
            setattr(proto, name, json.dumps(config.pop(name)))
    return proto


def convert_single_images_data_info_to_proto(config: dict) -> ImagesSingleDataInfo:
    """Convert a dictionary to single image data info proto message."""
    unstructured_params = convert_single_unstructured_params_to_proto(config)
    config_type = config.pop("type", "default")
    if config_type == "default":
        proto = ImagesSingleDataInfo(
            single_data_file_info=ImagesSingleDataFileInfo(
                file_name=config["file_name"]
            ),
            single_params=unstructured_params,
        )
    else:
        raise ValueError(f"Unsupported config type: {config_type}")
    if "load_path" in config and config["load_path"] is not None:
        proto.load_path = config["load_path"]
    return proto


def convert_images_data_info_to_proto(config: dict) -> ImagesDataInfo:
    """Convert config to proto message for images data."""
    config_type = config.get("type", "default")
    if config_type == "default":
        ref_config = copy.deepcopy(config)
        ref_config["file_name"] = config["ref_path"]
        eval_config = copy.deepcopy(config)
        eval_config["file_name"] = config["eval_path"]
        eval_data_info = convert_single_images_data_info_to_proto(eval_config)
        ref_data_info = convert_single_images_data_info_to_proto(ref_config)
    elif config_type == "split":
        eval_data_info = convert_single_images_data_info_to_proto(
            config["eval_data_info"]
        )
        ref_data_info = convert_single_images_data_info_to_proto(
            config["ref_data_info"]
        )
    else:
        raise ValueError(f"Unsupported config type: {config['type']}")
    return ImagesDataInfo(ref_data_info=ref_data_info, eval_data_info=eval_data_info)


def convert_images_config_to_proto(config: dict) -> ImagesCLIConfig:
    """Convert config to images proto."""
    # pop to remove from original config dict
    data_info = convert_images_data_info_to_proto(config.pop("data_info"))
    proto = ImagesCLIConfig(data_info=data_info)
    config_names = [field.name for field in ImagesCLIConfig.DESCRIPTOR.fields]
    for name in config_names:
        if name in config and config[name] is not None:
            # pop to remove from original config dict
            setattr(proto, name, json.dumps(config.pop(name)))
    return proto


def _update_key_names(config: dict) -> dict:
    """Update key names in config for backwards compatibility."""
    key_names = [
        ("test_config", "tests_config"),
        ("subset_profiling_config", "subset_profiling_info"),
    ]
    for old_name, new_name in key_names:
        if old_name in config:
            if new_name in config:
                raise ValueError(
                    f"Both {old_name} and {new_name} cannot be present in the config."
                )
            config[new_name] = config.pop(old_name)
    return config


def convert_config_to_proto(_config: dict, data_type: "DataType.V") -> TypedCLIConfig:
    """Convert a dictionary config to proto."""
    config = deepcopy(_config)
    config = _update_key_names(config)
    if data_type == DataType.TABULAR:
        tabular_config = convert_tabular_config_to_proto(config)
        proto = TypedCLIConfig(tabular_config=tabular_config)
    elif data_type == DataType.NLP:
        nlp_config = convert_nlp_config_to_proto(config)
        proto = TypedCLIConfig(nlp_config=nlp_config)
    elif data_type == DataType.IMAGES:
        images_config = convert_images_config_to_proto(config)
        proto = TypedCLIConfig(images_config=images_config)
    else:
        raise ValueError(f"Unknown data type: {data_type}")
    for name in config:
        if name not in config or config[name] is None:
            continue
        if name == "tests_config":
            setattr(proto, name, json.dumps(config[name]))
        else:
            setattr(proto, name, config[name])
    return proto


def convert_tabular_incremental_config_to_proto(
    config: dict,
) -> TabularIncrementalConfig:
    """Convert a dictionary incremental config to tabular incremental proto."""
    if "eval_data_info" in config:
        eval_data_info = convert_single_tabular_data_info_to_proto(
            config["eval_data_info"]
        )
        proto = TabularIncrementalConfig(eval_data_info=eval_data_info)
    elif "eval_path" in config:
        data_file_info = TabularSingleDataFileInfo(file_name=config["eval_path"],)
        tabular_params = TabularSingleDataInfoParams(
            timestamp_col=config["timestamp_col"]
        )
        if "eval_pred_path" in config:
            tabular_params.pred_path = config["eval_pred_path"]

        eval_data_info = TabularSingleDataInfo(
            single_data_file_info=data_file_info, single_params=tabular_params
        )
        proto = TabularIncrementalConfig(eval_data_info=eval_data_info)
    else:
        raise ValueError(f"Invalid incremental config: {config}")

    return proto


def convert_nlp_incremental_config_to_proto(config: dict) -> NLPIncrementalConfig:
    """Convert a dictionary incremental config to nlp incremental proto."""
    if "eval_data_info" in config:
        eval_data_info = convert_single_nlp_data_info_to_proto(config["eval_data_info"])
        proto = NLPIncrementalConfig(eval_data_info=eval_data_info)
    elif "eval_path" in config:
        # if config is in the old format, convert to use singledatainfo format
        data_file_info = NLPSingleDataFileInfo(file_name=config["eval_path"])
        eval_data_info = NLPSingleDataInfo(single_data_file_info=data_file_info)
        # NOTE: if eval_pred_path specified, create corresopnding prediction_info
        # in eval_data_info
        if "eval_pred_path" in config and config["eval_pred_path"] is not None:
            eval_data_info.single_params.prediction_info.CopyFrom(
                SinglePredictionInfo(path=config["eval_pred_path"])
            )

        proto = NLPIncrementalConfig(eval_data_info=eval_data_info)
    else:
        raise ValueError(f"Invalid incremental config: {config}")
    return proto


def convert_incremental_config_to_proto(
    _config: dict, data_type: "DataType.V"
) -> TypedIncrementalConfig:
    """Convert a dictionary incremental config to proto."""
    config = deepcopy(_config)
    # TODO: implement other modalities too
    if data_type == DataType.TABULAR:
        tabular_config = convert_tabular_incremental_config_to_proto(config)
        proto = TypedIncrementalConfig(tabular_incremental_config=tabular_config)
    elif data_type == DataType.NLP:
        nlp_config = convert_nlp_incremental_config_to_proto(config)
        proto = TypedIncrementalConfig(nlp_incremental_config=nlp_config)
    else:
        raise ValueError(f"Unknown data type: {data_type}")

    if "include_model" in config:
        setattr(proto, "include_model", config["include_model"])
    return proto


def proto_is_empty(proto_val: Any) -> bool:
    """Check if a proto is empty."""
    if isinstance(proto_val, Message):
        return proto_val == proto_val.__class__()
    return not bool(proto_val)
