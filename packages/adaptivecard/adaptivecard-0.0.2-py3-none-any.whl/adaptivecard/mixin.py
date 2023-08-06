import json
# from typing import get_type_hints, Union
# from typing_extensions import get_args, get_origin


class Mixin:    # essa é uma classe do tipo mixin. Não tem funcionalidade própria, serve para fornecer funcionalidade a outras classes.
    def create_fields(self, local_variables_dict) -> None:
        variables = [parameter for parameter in self.__init__.__code__.co_varnames if parameter != "self"]
        for variable in variables:
            value = local_variables_dict[variable]
            if value is not None:
                self.__dict__[variable] = value

    # def create_fields(self, local_variables_dict) -> None:
    #     variables = get_type_hints(self.__init__)
    #     for variable in variables:
    #         value = local_variables_dict[variable]
    #         expected_type = variables[variable]
    #         if value is not None:
    #             type_origin = get_origin(expected_type)
    #             if type_origin is None:
    #                 if type(value) != expected_type:
    #                     msg = "'{variable}' attribute cannot be of type '{data_type}'"
    #                     raise Exception(msg)
    #             elif type_origin == list:
    #                 if type(value) != list:
    #                     msg = ""
    #                     raise Exception(msg)
    #                 else:
    #                     expected_types_tuple = get_args(expected_type)
    #                     type_origins_list = [x if get_origin(x) is None else get_origin(x) for x in expected_types_tuple]
    #                     expected_types_inside_list = get_args(expected_types_tuple[type_origins_list.index(list)])
    #                     if get_origin(expected_types_inside_list)[0] == Union:
    #                         expected_types_inside_list = list(get_args(expected_types_inside_list[0]))
    #                     for i in range(len(expected_types_inside_list)):
    #                         if isinstance(expected_types_inside_list[i], str):
    #                             expected_types_inside_list[i] == eval(expected_types_inside_list[i])
    #                     for x in value:
    #                         if type(x) not in expected_types_inside_list:
    #                             msg = f"objects of type '{type(x)}' are not allowed in '{variable}' list"
    #                             raise Exception(msg)
    #             elif type_origin == Union:
    #                 expected_types_tuple = get_args(expected_type)
    #                 type_origins_list = [x if get_origin(x) is None else get_origin(x) for x in expected_types_tuple]
    #                 if type(value) not in type_origins_list:
    #                     msg = f"'{variable}' attribute cannot be of type {type(value)}"
    #                     raise Exception(msg)
    #                 elif type(value) == list:
    #                     expected_types_inside_list = get_args(expected_types_tuple[type_origins_list.index(list)])
    #                     if get_origin(expected_types_inside_list[0]) == Union:
    #                         expected_types_inside_list = list(get_args(expected_types_inside_list[0]))
    #                     for x in value:
    #                         if type(x) not in expected_types_inside_list:
    #                             msg = f"objects of type '{type(x)}' are not allowed in '{variable}' list"
    #                             raise Exception(msg)

    #             self.__dict__[variable] = value

    def to_dict(self):
        dic = json.loads(json.dumps(self, default=lambda obj: obj.__dict__))  # isso é um hack muito ixpertinho
        return dic

    def set_version(self, version: str) -> None:
        self.version = version
