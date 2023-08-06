from config_parser.base_config_model import BaseConfigModel
from config_parser.config_parser_enums.parameter_names import ParameterNames

'''
Config model describing a relationship that passes a single value to a parameter
'''


class SingleValueNavigationConfigModel(BaseConfigModel):
    def __init__(self, yaml_object: dict):
        super().__init__(yaml_object)

    def get_required_params(self):
        return {
            ParameterNames.parameter_reference: self.set_parameter_reference,
            ParameterNames.data_parameter: self.set_data_parameter
        }

    def get_optional_params(self):
        return {

        }

    def set_parameter_reference(self, value):
        self.parameter_reference = value

    def set_data_parameter(self, value):
        self.data_parameter = value
