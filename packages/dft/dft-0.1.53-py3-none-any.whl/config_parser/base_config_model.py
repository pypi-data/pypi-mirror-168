OPTIONAL_PARAMS = {}  # Example: {'param_name', 'default value']
REQUIRED_PARAMS = {}  # Example: {'param_name', 'Error message if not present'}

'''
Base config model to hold common pattern to parse df application configs.
'''


class BaseConfigModel:
    def __init__(self, yaml_object: dict):
        self.yaml_object = yaml_object
        self.optional_params = self.get_optional_params()
        self.required_params = self.get_required_params()
        self.validate_and_init()

    '''
    Validate the config to ensure if it only has the appropriate parameters
    '''

    def validate_and_init(self):
        # Validate basic sanity of the input params
        for param_name, value in self.yaml_object.items():
            required_param = self.required_params.get(param_name)
            optional_param = self.optional_params.get(param_name)
            if required_param is None and optional_param is None:
                available_params = list(self.required_params.keys())
                available_params.append(list(self.optional_params.keys()))
                raise ValueError(f"Invalid param `{param_name}` is passed. "
                                 f"Available params are: {available_params}")
            if required_param is not None and optional_param is not None:
                raise ValueError(f"`{param_name}` is present in both required and optional param list!")

        # Validate all required params are present & set those values are present
        for param_name, set_func in self.required_params.items():
            value_from_input = self.yaml_object.get(param_name)
            if value_from_input is None:
                raise ValueError(f"Required param `{param_name}` is missing in config!")
            set_func(value_from_input)

        # Set optional params
        for param_name, set_func in self.optional_params.items():
            value_from_input = self.yaml_object.get(param_name)
            set_func(value_from_input)

    def get_required_params(self):
        raise ValueError("It must be declared in the child class!")

    def get_optional_params(self):
        raise ValueError("It must be declared in the child class!")

    def to_json(self):
        json_dict = {}
        for param_name in self.required_params.keys():
            attr_val = getattr(self, param_name)
            json_dict = {
                **json_dict,
                param_name: attr_val
            }

        for param_name in self.optional_params.keys():
            attr_val = getattr(self, param_name)
            json_dict = {
                **json_dict,
                param_name: attr_val
            }

        return self.clean_json(json_dict)

    def clean_json(self, json_dict):
        clean_json = {}
        for key, item in json_dict.items():
            if isinstance(item, BaseConfigModel):
                clean_json = {**clean_json, key: item.to_json()}
            elif isinstance(item, list):
                clean_list = []
                for config in item:
                    if isinstance(config, BaseConfigModel):
                        config = config.to_json()
                    clean_list.append(config)
                clean_json = {**clean_json, key: clean_list}
            else:
                clean_json = {**clean_json, key: item}

        return clean_json
