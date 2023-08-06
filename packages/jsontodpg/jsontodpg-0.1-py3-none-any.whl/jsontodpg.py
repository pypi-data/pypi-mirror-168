from tokenizer import Tokenizer
from dpgkeywords import *
import dearpygui.dearpygui as dpg

FUNCTION_NAME = "name"
REFERENCE = "function reference"
ARGS = "args"
LEVEL = "level"
PARENT = "parent"
TAG = "tag"


def children(obj):
    """
    Iterate through and find child objects from input collection

    Args:
        obj (tuple,dict,list): the parent object.

    Returns:
        Children collections of input collection if they are tuple, dict or list.
    """

    collection_types = {
        "tuple": lambda obj: obj,
        "list": lambda obj: obj,
        "dict": lambda obj: obj.items(),
    }

    return [
        item
        for item in collection_types[type(obj).__name__](obj)
        if type(item).__name__ in collection_types
    ]


class JsonToDpg:
    def __init__(
        self,
        generate_keyword_file_name="",
        custom_modules=[],
        custom_functions={},
        use_dpg_extended=True,
    ):
        self.tokenizer = Tokenizer(
            generate_keyword_file_name=generate_keyword_file_name,
            custom_modules=custom_modules,
            custom_functions=custom_functions,
            use_dpg_extended=use_dpg_extended,
        )

    def __build_and_run(self, json_object):
        self.build_function_stack(json_object)
        # Run each function in stack
        # [function[REFERENCE](**function[ARGS]) for function in self.function_stack]
        for function in self.function_stack:

            function[REFERENCE](**function[ARGS])

    def parse(self, json_object):
        dpg.create_context()
        self.__build_and_run(json_object)
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.start_dearpygui()
        dpg.destroy_context()

    def get_parent(self, current_level):
        reverse_call_stack = self.function_stack[::-1]
        for i in range(len(reverse_call_stack)):
            last_item = reverse_call_stack[i]
            if (
                last_item[LEVEL] < current_level
                and not last_item[FUNCTION_NAME] == "viewport"
            ):
                return last_item[ARGS][TAG]
        return ""

    def build_function_stack(self, _object, level=0):

        # Reset call stack if somehow there is residual calls
        if level == 0:
            self.function_stack = []

        # Find Tuples, Dicts, and Lists in current object
        children_objects = children(_object)

        if isinstance(_object, tuple):
            object_name = _object[0]

            # Is Recognized Function
            if object_name in self.tokenizer.components:
                tag_name = f"{len(self.function_stack)}-{object_name}"
                self.__add_function_to_stack(object_name, level, tag_name)
                self.__assign_parent_and_tag(object_name, level, tag_name)

            # Is Recognized Parameter Of Function
            elif object_name in self.tokenizer.parameters:
                self.function_stack[-1][ARGS].update({object_name: _object[1]})

        # Dig into Tuples, Dicts, and Lists. Increment Level. Start Again.
        for child in children_objects:
            self.build_function_stack(_object=child, level=level + 1)

    def __add_function_to_stack(self, object_name, level, tag_name):

        self.function_stack.append(
            (
                {
                    FUNCTION_NAME: object_name,
                    REFERENCE: self.tokenizer.components[object_name],
                    TAG: tag_name,
                    LEVEL: level,
                    ARGS: {},
                }
            )
        )

    def __assign_parent_and_tag(self, object_name, level, tag_name):
        if PARENT in self.tokenizer.component_parameter_relations[object_name]:
            parent = self.get_parent(level)
            if parent:
                self.function_stack[-1][ARGS].update({PARENT: parent})
        if TAG in self.tokenizer.component_parameter_relations[object_name]:
            self.function_stack[-1][ARGS].update({TAG: tag_name})
