import enum
import operator as O
from dataclasses import dataclass
from datetime import datetime
from functools import reduce
from operator import attrgetter
from typing import Any, Callable, Collection, List, Optional, Tuple, Union

import pyspark.sql.functions as F
import pyspark.sql.types as T
from pyspark.sql import DataFrame, Observation, SparkSession
from pyspark.sql import Window as W

from . import dataframe as D


class CheckLevel(enum.Enum):
    WARNING = 0
    ERROR = 1


class CheckDataType(enum.Enum):
    AGNOSTIC = 0
    NUMERIC = 1
    STRING = 2
    DATE = 3
    TIME = 4


@dataclass(frozen=True)
class Rule:
    method: str
    column: Union[Tuple[str], str]
    value: Optional[Any]
    tag: str
    coverage: float = 1.0


class Check:
    COMPUTE_DELIMITER = chr(166)  # ¦

    def __init__(
        self, level: CheckLevel, name: str, execution_date: datetime = datetime.today()
    ):
        self._rules = []
        self._compute = {}
        self._unique = {}
        self.level = level
        self.name = name
        self.date = execution_date

    def _single_value_rule(
        column: str,
        value: Optional[Any],
        operator: Callable,
    ):
        return F.sum((operator(F.col(column), value)).cast("integer"))

    @staticmethod
    def inventory():
        """A full list of all rules available in the check"""
        return [
            "is_complete",
            "are_complate",
            "is_unique",
            "are_unique",
            "is_greater_than",
            "is_greater_or_equal_than",
            "is_less_than",
            "is_less_or_equal_than",
            "is_equal",
            "matches_regex",
            "has_min",
            "has_max",
            "has_std",
            "is_between",
            "is_contained_in",
            "has_percentile",
            "has_max_by",
            "has_min_by",
            "satisfies"
        ]

    def is_complete(self, column: str, pct: float = 1.0):
        """Validation for non-null values in column"""
        self._rules.append(
            Rule("is_complete", column, None, CheckDataType.AGNOSTIC, pct)
        )
        self._compute[
            f"is_complete{self.COMPUTE_DELIMITER}{column}{self.COMPUTE_DELIMITER}N/A{self.COMPUTE_DELIMITER}{pct}"
        ] = F.sum(F.col(column).isNotNull().cast("integer"))
        return self

    def are_complete(self, column: Tuple[str], pct: float = 1.0):
        """Validation for non-null values in a group of columns"""
        if isinstance(column, List):
            column = tuple(column)
        self._rules.append(
            Rule("are_complete", column, None, CheckDataType.AGNOSTIC, pct)
        )
        self._compute[
            f"are_complete{self.COMPUTE_DELIMITER}{column}{self.COMPUTE_DELIMITER}N/A{self.COMPUTE_DELIMITER}{pct}"
        ] = reduce(
            O.add, [F.sum(F.col(c).isNotNull().cast("integer")) for c in column]
        ) / len(
            column
        )
        return self

    def is_unique(self, column: str, pct: float = 1.0):
        """Validation for unique values in column"""
        self._rules.append(Rule("is_unique", column, CheckDataType.AGNOSTIC, pct))
        self._unique[
            f"is_unique{self.COMPUTE_DELIMITER}{column}{self.COMPUTE_DELIMITER}N/A{self.COMPUTE_DELIMITER}{pct}"
        ] = F.count_distinct(F.col(column))
        return self

    def are_unique(self, column: Tuple[str], pct: float = 1.0):
        """Validation for unique values in a group of columns"""
        if isinstance(column, List):
            column = tuple(column)
        self._rules.append(Rule("are_unique", column, CheckDataType.AGNOSTIC, pct))
        self._compute[
            f"are_unique{self.COMPUTE_DELIMITER}{column}{self.COMPUTE_DELIMITER}N/A{self.COMPUTE_DELIMITER}{pct}"
        ] = F.count_distinct(*[F.col(c) for c in column])
        return self

    def is_greater_than(self, column: str, value: float, pct: float = 1.0):
        """Validation for numeric greater than value"""
        self._rules.append(
            Rule("is_greater_than", column, value, CheckDataType.NUMERIC, pct)
        )
        self._compute[
            f"is_greater_than{self.COMPUTE_DELIMITER}{column}{self.COMPUTE_DELIMITER}{value}{self.COMPUTE_DELIMITER}{pct}"
        ] = self._single_value_rule(column, value, O.gt)
        return self

    def is_greater_or_equal_than(self, column: str, value: float, pct: float = 1.0):
        """Validation for numeric greater or equal than value"""
        self._rules.append(
            Rule("is_greater_or_equal_than", column, value, CheckDataType.NUMERIC, pct)
        )
        self._compute[
            f"is_greater_or_equal_than{self.COMPUTE_DELIMITER}{column}{self.COMPUTE_DELIMITER}{value}{self.COMPUTE_DELIMITER}{pct}"
        ] = self._single_value_rule(column, value, O.ge)
        return self

    def is_less_than(self, column: str, value: float, pct: float = 1.0):
        """Validation for numeric less than value"""
        self._rules.append(
            Rule("is_less_than", column, value, CheckDataType.NUMERIC, pct)
        )
        self._compute[
            f"is_less_than{self.COMPUTE_DELIMITER}{column}{self.COMPUTE_DELIMITER}{value}{self.COMPUTE_DELIMITER}{pct}"
        ] = self._single_value_rule(column, value, O.lt)
        return self

    def is_less_or_equal_than(self, column: str, value: float, pct: float = 1.0):
        """Validation for numeric less or equal than value"""
        self._rules.append(
            Rule("is_less_or_equal_than", column, value, CheckDataType.NUMERIC, pct)
        )
        self._compute[
            f"is_less_or_equal_than{self.COMPUTE_DELIMITER}{column}{self.COMPUTE_DELIMITER}{value}{self.COMPUTE_DELIMITER}{pct}"
        ] = self._single_value_rule(column, value, O.le)
        return self

    def is_equal(self, column: str, value: float, pct: float = 1.0):
        """Validation for numeric column equal than value"""
        self._rules.append(Rule("is_equal", column, value, CheckDataType.NUMERIC, pct))
        self._compute[
            f"is_equal{self.COMPUTE_DELIMITER}{column}{self.COMPUTE_DELIMITER}{value}{self.COMPUTE_DELIMITER}{pct}"
        ] = self._single_value_rule(column, value, O.eq)
        return self

    def matches_regex(self, column: str, value: str, pct: float = 1.0):
        """Validation for string type column matching regex expression"""
        self._rules.append(
            Rule("matches_regex", column, value, CheckDataType.STRING, pct)
        )
        self._compute[
            f"matches_regex{self.COMPUTE_DELIMITER}{column}{self.COMPUTE_DELIMITER}{value}{self.COMPUTE_DELIMITER}{pct}"
        ] = F.sum((F.length(F.regexp_extract(column, value, 0)) > 0).cast("integer"))
        return self

    def has_min(self, column: str, value: float, pct: float = 1.0):
        """Validation of a column’s minimum value"""
        self._rules.append(Rule("has_min", column, value, CheckDataType.NUMERIC))
        self._compute[
            f"has_min{self.COMPUTE_DELIMITER}{column}{self.COMPUTE_DELIMITER}{value}{self.COMPUTE_DELIMITER}{pct}"
        ] = (F.min(F.col(column)) == value)
        return self

    def has_max(self, column: str, value: float, pct: float = 1.0):
        """Validation of a column’s maximum value"""
        self._rules.append(Rule("has_max", column, value, CheckDataType.NUMERIC))
        self._compute[
            f"has_max{self.COMPUTE_DELIMITER}{column}{self.COMPUTE_DELIMITER}{value}{self.COMPUTE_DELIMITER}{pct}"
        ] = (F.max(F.col(column)) == value)
        return self

    def has_std(self, column: str, value: float, pct: float = 1.0):
        """Validation of a column’s standard deviation"""
        self._rules.append(Rule("has_std", column, value, CheckDataType.NUMERIC))
        self._compute[
            f"has_std{self.COMPUTE_DELIMITER}{column}{self.COMPUTE_DELIMITER}{value}{self.COMPUTE_DELIMITER}{pct}"
        ] = (F.stddev_pop(F.col(column)) == value)
        return self

    def is_between(self, column: str, *value: Any, pct: float = 1.0):
        """Validation of a column between a range"""
        self._rules.append(
            Rule("is_between", column, None, CheckDataType.AGNOSTIC, pct)
        )
        self._compute[
            f"is_between{self.COMPUTE_DELIMITER}{column}{self.COMPUTE_DELIMITER}{value}{self.COMPUTE_DELIMITER}{pct}"
        ] = F.sum(F.col(column).between(*value).cast("integer"))
        return self

    def is_contained_in(
        self, column: str, value: Tuple[str, int, float], pct: float = 1.0
    ):
        """Validation of column value in set of given values"""
        # Create tuple if user pass list
        if isinstance(value, List):
            value = tuple(value)

        # Check value type to later assess correct column type
        if [isinstance(v, str) for v in value]:
            check = CheckDataType.STRING
        else:
            check = CheckDataType.NUMERIC
        self._rules.append(Rule("is_contained_in", column, value, check))
        self._compute[
            f"is_contained_in{self.COMPUTE_DELIMITER}{column}{self.COMPUTE_DELIMITER}{value}{self.COMPUTE_DELIMITER}{pct}"
        ] = F.sum((F.col(column).isin(list(value))).cast("integer"))
        return self

    def has_percentile(
        self,
        column: str,
        value: float,
        percentile: float,
        precision: int = 10000,
        pct: float = 1.0,
    ):
        """Validation of a column percentile value"""
        self._rules.append(Rule("has_percentile", column, value, CheckDataType.NUMERIC))
        self._compute[
            f"has_percentile{self.COMPUTE_DELIMITER}{column}{self.COMPUTE_DELIMITER}{value}{self.COMPUTE_DELIMITER}{pct}"
        ] = (F.percentile_approx(column, percentile, precision) == value)
        return self

    def has_max_by(
        self, column_source: str, column_target: str, value: float, pct: float = 1.0
    ):
        """Validation of a column maximum based on other column maximum"""
        self._rules.append(
            Rule(
                "has_max_by",
                (column_source, column_target),
                value,
                CheckDataType.NUMERIC,
            )
        )
        self._compute[
            f"has_max_by{self.COMPUTE_DELIMITER}{column_source}/{column_target}{self.COMPUTE_DELIMITER}{value}{self.COMPUTE_DELIMITER}{pct}"
        ] = (F.max_by(column_target, column_source) == value)
        return self

    def has_min_by(
        self, column_source: str, column_target: str, value: float, pct: float = 1.0
    ):
        """Validation of a column minimum based on other column minimum"""
        self._rules.append(
            Rule(
                "has_min_by",
                (column_source, column_target),
                value,
                CheckDataType.NUMERIC,
            )
        )
        self._compute[
            f"has_min_by{self.COMPUTE_DELIMITER}{column_source}/{column_target}{self.COMPUTE_DELIMITER}{value}{self.COMPUTE_DELIMITER}{pct}"
        ] = (F.min_by(column_target, column_source) == value)
        return self

    def satisfies(self, predicate: str, pct: float = 1.0):
        """Validation of a column satisfying a SQL-like predicate"""
        self._rules.append(
            Rule(
                "satisfies",
                None,
                predicate,
                CheckDataType.AGNOSTIC,
            )
        )
        self._compute[
            f"satisfies{self.COMPUTE_DELIMITER}{predicate}{self.COMPUTE_DELIMITER}{self.COMPUTE_DELIMITER}{pct}"
        ] = F.sum(F.expr(predicate).cast("integer"))
        return self

    def __repr__(self):
        return f"Check(level:{self.level}, desc:{self.name}, rules:{len(set(self._rules))})"

    def validate(self, spark: SparkSession, dataframe: DataFrame):
        """Compute all rules in this check for specific data frame"""
        assert (
            self._rules
        ), "Check is empty. Add validations i.e. is_complete, is_unique, etc."

        assert isinstance(
            dataframe, DataFrame
        ), "Cualle operates only with Spark Dataframes"

        # Pre-validate columns
        rule_set = set(self._rules)
        single_columns = []
        for column_field in map(attrgetter("column"), rule_set):
            if isinstance(column_field, str):
                single_columns.append(column_field)
            elif isinstance(column_field, Collection):
                for column_in_group in column_field:
                    single_columns.append(column_in_group)

        column_set = set(single_columns)
        unknown_columns = column_set.difference(dataframe.columns)
        assert column_set.issubset(
            dataframe.columns
        ), f"Column(s): {unknown_columns} not in dataframe"

        # Pre-Validation of numeric data types
        numeric_rules = []
        for rule in rule_set:
            if rule.tag == CheckDataType.NUMERIC:
                if isinstance(rule.column, Collection):
                    for col in rule.column:
                        numeric_rules.append(col)
                elif isinstance(rule.column, str):
                    numeric_rules.append(rule.column)

        numeric_rules = set(numeric_rules)
        numeric_fields = D.numeric_fields(dataframe)
        non_numeric_columns = numeric_rules.difference(numeric_fields)
        assert set(numeric_rules).issubset(
            numeric_fields
        ), f"Column(s): {non_numeric_columns} are not numeric"

        # Create observation object
        observation = Observation(self.name)

        df_observation = dataframe.observe(
            observation,
            *[v.cast(T.StringType()).alias(k) for k, v in self._compute.items()],
        )
        rows = df_observation.count()

        unique_observe = (
            dataframe.select(
                *[v.cast(T.StringType()).alias(k) for k, v in self._unique.items()]
            )
            .first()
            .asDict()
        )

        return (
            spark.createDataFrame(
                [
                    tuple([i, *k])
                    for i, k in enumerate(
                        {**unique_observe, **observation.get}.items(), 1
                    )
                ],
                ["id", "computed_rule", "results"],
            )
            .withColumn(
                "pass_rate",
                F.round(
                    F.when(
                        (F.col("results") == "false") | (F.col("results") == "true"),
                        F.lit(1.0),
                    ).otherwise(F.col("results").cast(T.DoubleType()) / rows),
                    2,
                ),
            )
            .withColumn(
                "pass_threshold",
                F.split(F.col("computed_rule"), self.COMPUTE_DELIMITER).getItem(3),
            )
            .select(
                F.col("id"),
                F.lit(self.date.strftime("%Y-%m-%d")).alias("date"),
                F.lit(self.date.strftime("%H:%M:%S")).alias("time"),
                F.lit(self.name).alias("check"),
                F.lit(self.level.name).alias("level"),
                F.split(F.col("computed_rule"), self.COMPUTE_DELIMITER)
                .getItem(1)
                .alias("column"),
                F.split(F.col("computed_rule"), self.COMPUTE_DELIMITER)
                .getItem(0)
                .alias("rule"),
                F.split(F.col("computed_rule"), self.COMPUTE_DELIMITER)
                .getItem(2)
                .alias("value"),
                F.lit(rows).alias("rows"),
                "pass_rate",
                "pass_threshold",
                F.when(
                    (F.col("results") == "true")
                    | (
                        (F.col("results") != "false")
                        & (F.col("pass_rate") >= F.col("pass_threshold"))
                    ),
                    F.lit("PASS"),
                )
                .otherwise(F.lit("FAIL"))
                .alias("status"),
            )
        )
