from config_parser.base_config_model import BaseConfigModel
from config_parser.component_details_config_models.component_navigation_config_model import \
    ComponentNavigationConfigModel
from config_parser.component_details_config_models.input_component_config_model import InputComponentConfigModel
from config_parser.component_details_config_models.output_component_config_model import OutputComponentConfigModel
from config_parser.component_details_config_models.text_box_component_config_model import TextBoxComponentConfigModel
from config_parser.config_parser_enums.component_sizes import ComponentSize
from config_parser.config_parser_enums.component_types import ComponentTypes
from config_parser.config_parser_enums.parameter_names import ParameterNames


class ComponentConfigModel(BaseConfigModel):
    def __init__(self, yaml_object: dict):
        self.supported_types = [ComponentTypes.INPUT, ComponentTypes.OUTPUT, ComponentTypes.CHART,
                                ComponentTypes.TEXT_BOX]
        self.available_sizes = [ComponentSize.XS, ComponentSize.S, ComponentSize.M, ComponentSize.L, ComponentSize.XL]
        super().__init__(yaml_object)

    def get_optional_params(self):
        return {
            ParameterNames.navigation: self.set_navigation,
            ParameterNames.size: self.set_size,
            ParameterNames.label: self.set_label
        }

    def get_required_params(self):
        return {
            ParameterNames.type: self.set_type,
            ParameterNames.component_config: self.set_component_config
        }

    def set_type(self, value):
        if value not in self.supported_types:
            raise ValueError("Unsupported component type")

        self.type = value

    def set_component_config(self, value):
        if self.type == ComponentTypes.INPUT:
            self.component_config = InputComponentConfigModel(value)
        if self.type == ComponentTypes.CHART or self.type == ComponentTypes.OUTPUT:
            self.component_config = OutputComponentConfigModel(value)
        if self.type == ComponentTypes.TEXT_BOX:
            self.component_config = TextBoxComponentConfigModel(value)

    def set_navigation(self, value):
        if value is not None and self.type == ComponentTypes.INPUT:
            raise ValueError("Navigation from input component is not supported")
        if value is None:
            value = []

        if not isinstance(value, list):
            raise ValueError("Naviagtions must be a list")
        navigation = []
        for item in value:
            navigation.append(ComponentNavigationConfigModel(item))
        self.navigation = navigation

    def set_size(self, value):
        if value is None:
            value = ComponentSize.M
        if value not in self.available_sizes:
            raise ValueError("Unknown component size")
        self.size = value

    def set_label(self, value):
        self.label = value
