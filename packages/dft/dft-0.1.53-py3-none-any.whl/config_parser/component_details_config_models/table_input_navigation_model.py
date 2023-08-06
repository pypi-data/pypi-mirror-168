from config_parser.base_config_model import BaseConfigModel
from config_parser.config_parser_enums.parameter_names import ParameterNames


class TableInputNavigationModel(BaseConfigModel):

    def __init__(self, yaml_object: dict):
        super().__init__(yaml_object)

    def get_optional_params(self):
        return {

        }

    def get_required_params(self):
        return {
            ParameterNames.parameter_reference: self.set_parameter_reference
        }

    def set_parameter_reference(self, value):
        self.parameter_reference = value
