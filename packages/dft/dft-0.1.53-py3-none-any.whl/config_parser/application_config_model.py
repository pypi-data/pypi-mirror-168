from config_parser.application_flows_and_actions import ApplicationFlowsAndActionsModel
from config_parser.base_config_model import BaseConfigModel
from config_parser.component_config_model import ComponentConfigModel
from config_parser.config_parser_enums.parameter_names import ParameterNames
from config_parser.parameter_config_model import ParameterConfigModel


class ApplicationConfigModel(BaseConfigModel):
    def __init__(self, yaml_object: dict):
        super().__init__(yaml_object)

    def get_optional_params(self):
        return {
            ParameterNames.display_name: self.set_display_name,
            ParameterNames.description: self.set_description
        }

    def get_required_params(self):
        return {
            ParameterNames.name: self.set_name,
            ParameterNames.parameters: self.set_parameters,
            ParameterNames.flows_and_actions: self.set_flows_and_actions,
            ParameterNames.components: self.set_components,
        }

    def set_name(self, value):
        self.name = value

    def set_parameters(self, value):
        if not isinstance(value, list):
            raise ValueError("parameters to an application must be a list")

        parameters = []
        for parameter in value:
            parameters.append(ParameterConfigModel(parameter))

        self.parameters = parameters

    def set_flows_and_actions(self, value):
        if not isinstance(value, list):
            raise ValueError("Flows and actions to an application must be a list")

        flows_and_actions = []
        for item in value:
            flows_and_actions.append(ApplicationFlowsAndActionsModel(item))

        self.flows_and_actions = flows_and_actions

    def set_components(self, value):
        if not isinstance(value, list):
            raise ValueError("Components to an application must be a list")
        components = []
        for item in value:
            components.append(ComponentConfigModel(item))

        self.components = components

    def set_display_name(self, value):
        if value is None:
            value = self.name

        self.display_name = value

    def set_description(self, value):
        self.description = value

