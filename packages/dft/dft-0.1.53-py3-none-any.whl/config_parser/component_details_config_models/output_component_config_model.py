from config_parser.base_config_model import BaseConfigModel
from config_parser.config_parser_enums.parameter_names import ParameterNames

'''
Config Model for Output Type components, i.e, Execution Output and Charts.
'''


class OutputComponentConfigModel(BaseConfigModel):
    def __init__(self, yaml_object: dict):
        super().__init__(yaml_object)

    def get_optional_params(self):
        return {
            ParameterNames.source: self.set_source,
            ParameterNames.flow_index: self.set_flow_index
        }

    def get_required_params(self):
        return {
            ParameterNames.action_reference: self.set_action_reference
        }

    def set_source(self, value):
        self.source = value

    def set_flow_index(self, value):
        if value is None:
            self.flow_index = None
            return

        if not isinstance(value, int):
            raise ValueError("Flow index must be integer")

        self.flow_index = value

    def set_action_reference(self, value):
        self.action_reference = value
