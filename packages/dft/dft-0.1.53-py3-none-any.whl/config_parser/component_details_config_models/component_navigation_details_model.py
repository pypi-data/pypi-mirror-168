from config_parser.base_config_model import BaseConfigModel
from config_parser.component_details_config_models.single_value_navigation_config_model import \
    SingleValueNavigationConfigModel
from config_parser.component_details_config_models.table_input_navigation_model import TableInputNavigationModel
from config_parser.config_parser_enums.component_relationship_types import ComponentRelationshipTypes
from config_parser.config_parser_enums.parameter_names import ParameterNames


class ComponentNavigationDetailsModel(BaseConfigModel):

    def __init__(self, yaml_object: dict):
        self.available_type = [ComponentRelationshipTypes.CHART_CLICK, ComponentRelationshipTypes.TABLE_INPUT,
                               ComponentRelationshipTypes.CELL_INPUT, ComponentRelationshipTypes.CHART_DATA_INPUT]
        super().__init__(yaml_object)

    def get_optional_params(self):
        return {

        }

    def get_required_params(self):
        return {
            ParameterNames.type: self.set_type,
            ParameterNames.config: self.set_config,
            ParameterNames.reference: self.set_reference
        }

    def set_type(self, value):
        if value not in self.available_type:
            raise ValueError("Navigation type unknown")

        self.type = value

    def set_config(self, value):
        if self.type == ComponentRelationshipTypes.CHART_CLICK or self.type == ComponentRelationshipTypes.CELL_INPUT:
            self.config = SingleValueNavigationConfigModel(value)
        elif self.type == ComponentRelationshipTypes.TABLE_INPUT or self.type == ComponentRelationshipTypes.CHART_DATA_INPUT:
            self.config = TableInputNavigationModel(value)

    def set_reference(self, value):
        self.reference = value