import warnings

import numpy as np

from great_expectations.execution_engine import (
    PandasExecutionEngine,
    SparkDFExecutionEngine,
)
from great_expectations.execution_engine.sqlalchemy_execution_engine import (
    SqlAlchemyExecutionEngine,
)
from great_expectations.expectations.metrics.import_manager import F
from great_expectations.expectations.metrics.map_metric_provider import (
    ColumnMapMetricProvider,
    column_condition_partial,
)


class ColumnValuesInSet(ColumnMapMetricProvider):
    condition_metric_name = "column_values.in_set"
    condition_value_keys = ("value_set",)

    @column_condition_partial(engine=PandasExecutionEngine)
    def _pandas(cls, column, value_set, parse_strings_as_datetimes=None, **kwargs):
        # no need to parse as datetime; just compare the strings as-is
        if parse_strings_as_datetimes:
            warnings.warn(
                """The parameter "parse_strings_as_datetimes" is no longer supported and \
will be deprecated in a future release. Please update code accordingly.
""",
                DeprecationWarning,
            )

        if value_set is None:
            # Vacuously true
            return np.ones(len(column), dtype=np.bool_)
        return column.isin(value_set)

    @column_condition_partial(engine=SqlAlchemyExecutionEngine)
    def _sqlalchemy(cls, column, value_set, parse_strings_as_datetimes=None, **kwargs):
        if parse_strings_as_datetimes:
            raise NotImplementedError

        if value_set is None:
            # vacuously true
            return True
        elif len(value_set) == 0:
            return False
        return column.in_(value_set)

    @column_condition_partial(engine=SparkDFExecutionEngine)
    def _spark(cls, column, value_set, parse_strings_as_datetimes=None, **kwargs):
        if parse_strings_as_datetimes:
            # no need to parse as datetime; just compare the strings as-is
            warnings.warn(
                """The parameter "parse_strings_as_datetimes" is no longer supported and \
will be deprecated in a future release. Please update code accordingly.
""",
                DeprecationWarning,
            )

        if value_set is None:
            # vacuously true
            return F.lit(True)
        return column.isin(value_set)
