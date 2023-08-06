"""Utility functions for converting between SDK args and proto objects."""

from copy import deepcopy
from typing import Any, Dict, List, Optional, cast

from google.protobuf.json_format import ParseDict
from google.protobuf.message import Message

from rime_sdk.protos.firewall.firewall_pb2 import (
    BinSize,
    CustomLoaderArgs,
    DataLocation,
    DataLocationType,
    DeltaLakeArgs,
)
from rime_sdk.protos.result_synthesizer.result_message_pb2 import (
    DataType,
    ThresholdDirection,
    ThresholdInfo,
)
from rime_sdk.protos.schema.cli_config.cli_config_pb2 import (
    TabularSingleDataInfoParams,
    UnstructuredSingleDataInfoParams,
)


def proto_is_empty(proto_val: Any) -> bool:
    """Check if a proto is empty."""
    if isinstance(proto_val, Message):
        return proto_val == proto_val.__class__()
    return not bool(proto_val)


def get_bin_size_proto(bin_size_str: str) -> BinSize:
    """Get bin size proto from string."""
    years = 0
    months = 0
    seconds = 0
    if bin_size_str == "year":
        years += 1
    elif bin_size_str == "month":
        months += 1
    elif bin_size_str == "week":
        seconds += 7 * 24 * 60 * 60
    elif bin_size_str == "day":
        seconds += 24 * 60 * 60
    elif bin_size_str == "hour":
        seconds += 60 * 60
    else:
        raise ValueError(
            f"Got unknown bin size ({bin_size_str}), "
            f"should be one of: `year`, `month`, `week`, `day`, `hour`"
        )
    return BinSize(years=years, months=months, seconds=seconds)


TYPE_KEY = "enum_type"
PROTO_FIELD_KEY = "proto_field"
PROTO_TYPE_KEY = "proto_type"
LOCATION_TYPE_MAP: Dict[str, Dict] = {
    "data_collector": {TYPE_KEY: DataLocationType.LOCATION_TYPE_DATA_COLLECTOR},
    "delta_lake": {
        TYPE_KEY: DataLocationType.LOCATION_TYPE_DELTA_LAKE,
        PROTO_FIELD_KEY: "delta_lake_args",
        PROTO_TYPE_KEY: DeltaLakeArgs,
    },
    "custom_loader": {
        TYPE_KEY: DataLocationType.LOCATION_TYPE_CUSTOM_LOADER,
        PROTO_FIELD_KEY: "custom_loader_args",
        PROTO_TYPE_KEY: CustomLoaderArgs,
    },
}

DATA_TYPE_TO_PARAMS_MAP: Dict["DataType.V", Dict] = {
    DataType.TABULAR: {
        PROTO_FIELD_KEY: "tabular_params",
        PROTO_TYPE_KEY: TabularSingleDataInfoParams,
    },
    DataType.NLP: {
        PROTO_FIELD_KEY: "unstructured_params",
        PROTO_TYPE_KEY: UnstructuredSingleDataInfoParams,
    },
}


def location_args_to_data_location(
    location_type: str,
    location_info: Optional[Dict],
    data_params: Optional[Dict] = None,
    data_type: Optional["DataType.V"] = None,
) -> DataLocation:
    """Create Data Location object for Firewall Requests."""
    location_keys = set(LOCATION_TYPE_MAP.keys())
    if location_type not in location_keys:
        raise ValueError(
            f"Location type {location_type} must be one of {location_keys}"
        )
    location_enum = LOCATION_TYPE_MAP[location_type][TYPE_KEY]
    data_location = DataLocation(location_type=location_enum)

    proto_field = LOCATION_TYPE_MAP[location_type].get(PROTO_FIELD_KEY, None)
    proto_type = LOCATION_TYPE_MAP[location_type].get(PROTO_TYPE_KEY, None)
    if proto_type is not None and location_info is None:
        raise ValueError(
            "Must specify args for location info if setting location type "
            f"to {location_type}. See documentation for details"
        )

    if proto_field is not None and proto_type is not None:
        location_args_obj = ParseDict(location_info, proto_type())
        getattr(data_location, proto_field).CopyFrom(location_args_obj)
    if data_params is None:
        return data_location

    # Process the data parameters
    if data_type is None:
        raise ValueError("Must specify data type when specifying data params")
    if data_type not in DATA_TYPE_TO_PARAMS_MAP:
        raise ValueError(
            f"Specifying data params for {data_type} is not current supported"
        )

    proto_field = DATA_TYPE_TO_PARAMS_MAP[data_type].get(PROTO_FIELD_KEY)
    data_proto_field = cast(str, proto_field)
    data_proto_type: Any = DATA_TYPE_TO_PARAMS_MAP[data_type].get(PROTO_TYPE_KEY)
    data_params_object = ParseDict(data_params, data_proto_type())
    getattr(data_location.data_params, data_proto_field).CopyFrom(data_params_object)

    return data_location


THRESHOLD_INFO_TO_ENUM_MAP = {
    "above": ThresholdDirection.THRESHOLD_DIRECTION_ABOVE,
    "below": ThresholdDirection.THRESHOLD_DIRECTION_BELOW,
    None: ThresholdDirection.THRESHOLD_DIRECTION_UNSPECIFIED,
}


def get_threshold_direction_proto(direction: Optional[str]) -> "ThresholdDirection.V":
    """Get the threshold direction protobuf."""
    _direction = THRESHOLD_INFO_TO_ENUM_MAP.get(direction)
    if _direction is None:
        # TODO: Handle "both" cases
        raise ValueError(
            f"Invalid threshold direction {direction}. Expected 'above' or 'below'."
        )
    return _direction


def get_threshold_info_proto(metric_threshold_info: dict) -> ThresholdInfo:
    """Return the threshold info map."""
    info_copy = deepcopy(metric_threshold_info)
    info_copy["direction"] = get_threshold_direction_proto(
        metric_threshold_info.get("direction")
    )
    return ParseDict(info_copy, ThresholdInfo())


def threshold_infos_to_map(
    threshold_infos: List[ThresholdInfo],
) -> Dict[str, ThresholdInfo]:
    """Return map of metric name to ThresholdInfo."""
    threshold_info_map = {}
    for threshold_info in threshold_infos:
        info_without_metric = ThresholdInfo(
            direction=threshold_info.direction,
            low=threshold_info.low,
            medium=threshold_info.medium,
            high=threshold_info.high,
            disabled=threshold_info.disabled,
        )
        threshold_info_map[threshold_info.metric_name] = info_without_metric
    return threshold_info_map


DEFAULT_THRESHOLD_INFO_KEY_ORDER = [
    field.name for field in ThresholdInfo.DESCRIPTOR.fields
]
# Put metric_name at the beginning
DEFAULT_THRESHOLD_INFO_KEY_ORDER.remove("metric_name")
DEFAULT_THRESHOLD_INFO_KEY_ORDER = ["metric_name"] + DEFAULT_THRESHOLD_INFO_KEY_ORDER


def get_data_type_enum(data_type: str) -> "DataType.V":
    """Get data type enum value from string."""
    if data_type == "tabular":
        return DataType.TABULAR
    elif data_type == "nlp":
        return DataType.NLP
    elif data_type == "images":
        return DataType.IMAGES
    else:
        raise ValueError(
            f"Got unknown data type ({data_type}), "
            f"should be one of: `tabular`, `nlp`, `images`"
        )
