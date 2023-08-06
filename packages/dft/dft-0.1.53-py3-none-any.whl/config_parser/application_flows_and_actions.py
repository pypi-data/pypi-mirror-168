from config_parser.base_config_model import BaseConfigModel
from config_parser.config_parser_enums.parameter_names import ParameterNames
from config_parser.flow_parameter_config_model import FlowParameterConfigModel


class ApplicationFlowsAndActionsModel(BaseConfigModel):
    def __init__(self, yaml_object: dict):
        super().__init__(yaml_object)

    def get_required_params(self):
        return {
            ParameterNames.action_reference: self.set_action_reference,
            ParameterNames.unique_name: self.set_unique_name,
            ParameterNames.parameter_config: self.set_parameter_config
        }

    def get_optional_params(self):
        return {

        }

    def set_action_reference(self, value):
        self.action_reference = value

    def set_unique_name(self, value):
        self.unique_name = value

    def set_parameter_config(self, value):
        if not isinstance(value, list):
            raise ValueError("Parameter Config of flow/action should be a list")

        params = []
        for param in value:
            params.append(FlowParameterConfigModel(param))

        self.parameter_config = params

