from dataclasses import field
from typing import List

import marshmallow_dataclass
from marshmallow_dataclass import dataclass

from dft.models.chart_options.chart_options import ChartOptions

@dataclass
class SankeyChartOptions(ChartOptions):
    nodes: List[str] = field(metadata={"required": True}, default_factory=list)
    source: List[str] = field(metadata={"required": True}, default_factory=list)
    target: List[str] = field(metadata={"required": True}, default_factory=list)
    value: List[int] = field(metadata={"required": True}, default_factory=list)

    def __init__(self, nodes, source, target, value):
        self.nodes = nodes
        self.source = source
        self.target = target
        self.value = value

    def to_dict(self):
        model_schema = marshmallow_dataclass.class_schema(SankeyChartOptions)()
        return model_schema.dumps(self, many=False)
