from dataclasses import field
from typing import List

import marshmallow_dataclass
from marshmallow import post_dump
from marshmallow_dataclass import dataclass
from dft.models.chart_options.chart_options import ChartOptions

@dataclass
class RadarChartDataOptions(ChartOptions):
    dimension_column: str = field(metadata={"required": True})
    axis_columns: List[str] = field(metadata={"required": True}, default_factory=list)

    def __init__(self, dimension_column, axis_columns):
        self.dimension_column = dimension_column
        self.axis_columns = axis_columns

    @post_dump
    def clean_missing(self, data, **kwargs):
        removed_missing_fields = {k:v for (k,v) in data.items() if v is not None}
        return removed_missing_fields

    def to_dict(self):
        model_schema = marshmallow_dataclass.class_schema(RadarChartDataOptions)()
        return model_schema.dumps(self, many=False)
