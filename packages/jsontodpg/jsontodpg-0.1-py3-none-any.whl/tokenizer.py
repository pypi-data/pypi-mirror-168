import dearpygui.dearpygui as dpg
from collections import OrderedDict
import dpgextended as dpg_extended


DEFAULT_ALTERING_KEYWORD_FILTERS = ["add_", "create_"]
DEFAULT_NON_ALTERING_KEYWORD_FILTERS = ["draw", "load_"]
KEYWORD_IGNORE_SUBSTRINGS = ["mv", "__", "set", "dpg"]

SHARED_PYTHON_KEYWORDS = ["format"]


def clean_keyword(current_item):
    if current_item[0].isnumeric() or current_item in SHARED_PYTHON_KEYWORDS:
        return f"_{current_item}"
    return current_item


def clean_keywords_list(_list):
    for i in range(len(_list)):
        _list[i] = clean_keyword(_list[i])
    return _list


def remove_quotes(obj):
    return str(obj).replace('"', "").replace("'", "")


def write_to_py_file(file_path="", file_name="generated_python_file", data=""):
    temp_path = file_path + file_name + ".py"
    with open(temp_path, "w") as f:
        f.write(data)


def check_for_substrings(string, comparison_list, return_difference=False):
    if not [sub for sub in KEYWORD_IGNORE_SUBSTRINGS if (sub in string)]:
        for sub in comparison_list:
            if sub in string:
                if return_difference:
                    return string.replace(sub, "")
                return string


class Tokenizer:
    def __init__(
        self,
        generate_keyword_file_name="",
        custom_modules=[],
        custom_functions={},
        use_dpg_extended=True,
    ):

        # Which parameters can be used with each set of parameters
        self.component_parameter_relations = OrderedDict()
        self.components = {}
        self.parameters = []
        self.custom_functions = {}
        # ---------------------------
        self.build_keyword_library(
            dpg,
            altering_filters=DEFAULT_ALTERING_KEYWORD_FILTERS,
            non_altering_filters=DEFAULT_NON_ALTERING_KEYWORD_FILTERS,
        )

        if use_dpg_extended:
            self.build_keyword_library(dpg_extended)

        if generate_keyword_file_name:
            self.write_to_file(generate_keyword_file_name)

    def __filter_keyword(
        self, function_name, altering_filters=[], non_altering_filters=[]
    ):
        """
            Not all dearpygui functions make sense in json format.
            This checks against the desired substrings.
            e.g. functions starting with substring 'create_'.

        Args:
            filtered_keyword (str, optional):
        """
        if not altering_filters and not non_altering_filters:
            if not [sub for sub in KEYWORD_IGNORE_SUBSTRINGS if (sub in function_name)]:
                if not function_name == function_name.upper():
                    return function_name

        if altering_filters:
            filtered_keyword = check_for_substrings(
                function_name, altering_filters, return_difference=True
            )
            if filtered_keyword:

                return filtered_keyword

        if non_altering_filters:
            filtered_keyword = check_for_substrings(function_name, non_altering_filters)
            if filtered_keyword:
                return filtered_keyword

    def build_keyword_library(
        self,
        package,
        altering_filters=[],
        non_altering_filters=[],
    ):

        for function_name in dir(package):
            filtered_keyword = self.__filter_keyword(
                function_name, altering_filters, non_altering_filters
            )

            if filtered_keyword:

                filtered_keyword = clean_keyword(filtered_keyword)
                function_reference = getattr(package, function_name)
                self.components[filtered_keyword] = function_reference

                params = clean_keywords_list(
                    [
                        param
                        for param in function_reference.__code__.co_varnames
                        if not param in ["args", "kwargs"]
                    ]
                )

                # Add non-existing parameters to master parameter list
                self.parameters = self.parameters + [
                    param for param in params if not param in self.parameters
                ]

                self.component_parameter_relations[filtered_keyword] = params

    def write_to_file(self, file_name):
        string = "#THIS FILE WAS GENERATED\n"
        components = list(self.components.keys())

        string = (
            string + f"#--------------COMPONENTS--------------[{len(components)}]\n"
        )

        for component in components:
            string = string + "\n" + f'{component}="{component}"'

        string = (
            string
            + "\n"
            + f"\n#--------------PARAMETERS--------------[{len(self.parameters)}]\n"
        )

        for param in self.parameters:
            string = string + "\n" + f'{param}="{param}"'

        string = (
            string
            + "\n\n"
            + f"component_parameter_relations = {remove_quotes(str(dict(self.component_parameter_relations)))}"
        )
        string = string + "\n" + f"__all__ = {components + self.parameters}"

        write_to_py_file(file_name=file_name, data=string)
