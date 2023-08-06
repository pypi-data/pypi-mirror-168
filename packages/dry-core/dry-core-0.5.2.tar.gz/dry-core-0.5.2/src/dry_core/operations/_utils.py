import inspect
from typing import Callable, get_args, Union, get_origin

from ._models import FunctionInformation, FunctionArgInfo


def parse_function_information(
    function: Callable,
) -> FunctionInformation:
    return FunctionInformation(
        function_object=function,
        args=parse_function_parameters(function),
    )


def _parse_annotation_to_types_list(annotation) -> list:
    if get_origin(annotation) is Union:
        annotations = []
        for union_item in get_args(annotation):
            if union_item:
                annotations += _parse_annotation_to_types_list(union_item)
            else:
                annotations.append(None)
        return list(set(annotations))
    return [annotation]


def _parse_types_by_parameter(parameter):
    annotation = parameter.annotation
    # if no annotation provided
    if annotation is inspect.Parameter.empty:
        return None
    # if Union type annotation convert to Union args
    # else convert to list of 1 element
    elif get_origin(annotation) is Union:
        types = _parse_annotation_to_types_list(annotation)
    # if simple type
    else:
        types = [annotation]
    return list(set(types))


def parse_function_parameters(
    function: Callable,
) -> dict[str, FunctionArgInfo]:

    return {
        parameter.name: FunctionArgInfo(
            name=parameter.name,
            types=_parse_types_by_parameter(parameter),
            default_value=parameter.default if parameter.default is not inspect.Parameter.empty else ...,
        )
        for _, parameter in inspect.signature(function).parameters.items()
    }
