from config_parser.base_config_model import BaseConfigModel
from config_parser.component_details_config_models.component_navigation_details_model import \
    ComponentNavigationDetailsModel
from config_parser.config_parser_enums.available_component_navigation_sources import AvailableComponentNavigationSources
from config_parser.config_parser_enums.parameter_names import ParameterNames


class ComponentNavigationConfigModel(BaseConfigModel):
    def __init__(self, yaml_object: dict):
        self.available_destinations = [AvailableComponentNavigationSources.FLOW,
                                       AvailableComponentNavigationSources.ACTION,
                                       AvailableComponentNavigationSources.APPLICATION]
        super().__init__(yaml_object)

    def get_optional_params(self):
        return {
            ParameterNames.name: self.set_name
        }

    def get_required_params(self):
        return {
            ParameterNames.navigate_to: self.set_navigate_to,
            ParameterNames.navigation_details: self.set_navigation_details,
        }

    def set_name(self, value):
        self.name = value

    def set_navigate_to(self, value):
        if value not in self.available_destinations:
            raise ValueError(f"Navigate to {value} is not supported")
        self.navigate_to = value

    def set_navigation_details(self, value):
        self.navigation_details = ComponentNavigationDetailsModel(value)
