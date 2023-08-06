"""Library for converting Protobufs to Python data types such as dataframes."""
import re
from typing import Dict, Union

import numpy as np
import pandas as pd
from google.protobuf import empty_pb2
from google.protobuf.json_format import MessageToDict

from rime_sdk.protos.result_synthesizer.result_message_pb2 import TestCaseMetricCategory
from rime_sdk.protos.test_run_results.test_run_results_pb2 import (
    TestBatchResult,
    TestCase,
    TestRunDetail,
)

MODEL_PERF_REGEX = r"^metrics\.model_perf.*(ref_metric|eval_metric)$"

# Map of flattened field paths to their types in the Dataframe.
default_test_run_column_info = {
    # Metadata.
    "test_run_id": "str",
    "name": "str",
    "project_id": "str",
    "model_task": "str",  # OPTIONAL
    # The canonical JSON encoding converts enums to their string representations
    # so we do not need to do manual conversions.
    "data_type": "str",
    "testing_type": "str",
    "upload_time": "str",
    # Model source info.
    "model_source_info.name": "str",  # OPTIONAL
    # Data source info.
    "data_source_info.ref.name": "str",
    "data_source_info.eval.name": "str",
    # Metrics.
    "metrics.duration_millis": "Int64",
    "metrics.num_inputs": "Int64",
    "metrics.num_failing_inputs": "Int64",
    "metrics.summary_counts.total": "Int64",
    "metrics.summary_counts.pass": "Int64",
    "metrics.summary_counts.warning": "Int64",
    "metrics.summary_counts.fail": "Int64",
    "metrics.summary_counts.skip": "Int64",
    "metrics.severity_counts.num_none_severity": "Int64",
    "metrics.severity_counts.num_low_severity": "Int64",
    "metrics.severity_counts.num_medium_severity": "Int64",
    "metrics.severity_counts.num_high_severity": "Int64",
}

# List of all the columns to hide for a test batch DF.
TEST_BATCH_KEYS_TO_HIDE = [
    "show_in_test_comparisons",
    "failing_rows_results",
    "display",
]

# List of all the columns to hide for a test case DF.
TEST_CASE_KEYS_TO_HIDE = [
    "display",
    "feature_id",
    "test_case_id",
]

# TestBatchResult columns that need to be converted from string to int64
INT_TEST_BATCH_ATTRIBUTES = [
    "duration_in_millis",
    "summary_counts.total",
    "summary_counts.warning",
    "summary_counts.pass",
    "summary_counts.fail",
    "summary_counts.skip",
]

# Separator to use when flattening JSON into a dataframe.
# columns_to_keep definition relies on this separator.
DF_FLATTEN_SEPARATOR = "."


def parse_test_run_metadata(test_run: TestRunDetail) -> pd.DataFrame:
    """Parse test run metadata Protobuf message into a Pandas dataframe.

    The columns are not guaranteed to be returned in sorted order.
    Some values are optional and will appear as a NaN value in the dataframe.

    Results can be fixed to a version by providing the keyword argument `version`.
    """
    # Use the canonical JSON encoding for Protobuf messages.
    test_run_dict = MessageToDict(
        test_run,
        # including_default_value_fields only operates at the highest level of nesting -
        # it does not traverse subtrees of nested messages.
        # For example, if metrics.summary_counts is None, then none of its value will be
        # filled in with zeros.
        including_default_value_fields=True,
        # This ensures that the field names will be snake_case.
        preserving_proto_field_name=True,
    )

    # Flatten out nested fields in the Protobuf message.
    # The DF column name will be the field path joined by the `df_flatten_separator.`
    normalized_df = pd.json_normalize(test_run_dict, sep=DF_FLATTEN_SEPARATOR)

    default_test_run_columns = list(default_test_run_column_info.keys())

    # Include the model perf columns with the set of DF columns.
    # These are metrics like "Accuracy" over the reference and eval datasets.
    model_perf_columns = [c for c in normalized_df if re.match(MODEL_PERF_REGEX, c)]
    all_test_run_columns = default_test_run_columns + model_perf_columns

    missing_columns = set(all_test_run_columns).difference(set(normalized_df.columns))
    intersect_df = normalized_df[
        normalized_df.columns.intersection(all_test_run_columns)
    ]

    # Fill in the missing columns with None values.
    kwargs: Dict[str, None] = {}
    for column in missing_columns:
        kwargs[column] = None
    # Note that this step does not preserve column order.
    full_df = intersect_df.assign(**kwargs)

    non_default_cols = list(
        set(all_test_run_columns).difference(set(default_test_run_columns))
    )
    ordered_index = pd.Index(default_test_run_columns + sorted(non_default_cols))

    # The canonical Protobuf<>JSON encoding converts int64 values to string,
    # so we need to convert them back.
    # https://developers.google.com/protocol-buffers/docs/proto3#json
    # Note the type of all model perf metrics should be float64 so we do not have
    # to do this conversion.
    for key, value in default_test_run_column_info.items():
        if value == "Int64":
            # Some nested fields such as `metrics.severity_counts.low` will be `None`
            # because MessageToDict does not populate nested primitive fields with
            # default values.
            # Since some columns may be `None`, we must convert to `float` first.
            # https://stackoverflow.com/questions/60024262/error-converting-object-string-to-int32-typeerror-object-cannot-be-converted  # pylint: disable=line-too-long
            full_df[key] = full_df[key].astype("float").astype("Int64")

    return full_df.reindex(ordered_index, axis=1)


def parse_test_batch_result(
    raw_result: TestBatchResult, unpack_metrics: bool = False,
) -> pd.Series:
    """Parse test batch result into a series."""
    result_dict = MessageToDict(
        raw_result,
        including_default_value_fields=True,
        preserving_proto_field_name=True,
    )
    del result_dict["metrics"]
    if unpack_metrics:
        _add_metric_cols(result_dict, raw_result)

    # Note: some keys may be missing for nested singular messages, so we do
    # a safe delete here.
    for key in TEST_BATCH_KEYS_TO_HIDE:
        result_dict.pop(key, None)

    df = pd.json_normalize(result_dict, sep=DF_FLATTEN_SEPARATOR)

    for key in INT_TEST_BATCH_ATTRIBUTES:
        # Some nested fields such as `metrics.severity_counts.low` will be `None`
        # because MessageToDict does not populate nested primitive fields with
        # default values.
        # Since some columns may be `None`, we must convert to `float` first.
        # https://stackoverflow.com/questions/60024262/error-converting-object-string-to-int32-typeerror-object-cannot-be-converted  # pylint: disable=line-too-long
        df[key] = df[key].astype("float").astype("Int64")

    return df.squeeze(axis=0)


def parse_test_case_result(raw_result: TestCase, unpack_metrics: bool = False) -> dict:
    """Parse proto test case result to pythonic form."""
    result_dict = MessageToDict(
        raw_result,
        including_default_value_fields=True,
        preserving_proto_field_name=True,
    )
    del result_dict["metrics"]
    if unpack_metrics:
        _add_metric_cols(result_dict, raw_result)

    # Drop the keys to hide if they are specified.
    # Note: some keys may be missing for nested singular messages, so we do
    # a safe delete here.
    for key in TEST_CASE_KEYS_TO_HIDE:
        result_dict.pop(key, None)

    return result_dict


def _add_metric_cols(
    result_dict: dict, raw_result: Union[TestCase, TestBatchResult],
) -> None:
    """Unpack test metrics into separate fields."""
    for metric in raw_result.metrics:
        category_string = TestCaseMetricCategory.Name(metric.category)
        prefix = "TEST_CASE_METRIC_CATEGORY_"
        category_string = category_string[len(prefix) :]
        data_key = metric.WhichOneof("data")
        if data_key is None:
            metric_value = np.nan
        else:
            metric_value = getattr(metric, data_key)
            if isinstance(metric_value, empty_pb2.Empty):
                metric_value = np.nan
        if isinstance(metric_value, empty_pb2.Empty):
            metric_value = np.nan
        result_dict[f"{category_string}:{metric.metric}"] = metric_value
