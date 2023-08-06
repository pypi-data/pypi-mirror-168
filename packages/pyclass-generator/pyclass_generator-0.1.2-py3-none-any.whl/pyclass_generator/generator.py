import os
import re
import string
from pathlib import Path
from typing import List

import libcst as cst

from .cst import BaseCST
from .utils import validation


class Generator(BaseCST):
    def __init__(self, *args, **kwargs) -> None:
        self.classname: str = args[0].get('class').get('name')
        self.description: str = args[0].get('class').get('description')
        self.base_classes: List[str] = args[0].get('class').get('base_classes')
        self.class_attributes: dict = args[0].get('class').get('class_attributes')
        self.instance_attributes: dict = args[0].get('class').get('instance_attributes')
        self.instance_methods: dict = args[0].get('class').get('instance_methods')

    @property
    def class_name(self) -> str:
        name = re.sub(r"[^a-zA-Z0-9 ]", "", self.classname)
        name = name.translate({ord(c): None for c in string.whitespace})
        return name.capitalize()

    @property
    def class_description_CST(self) -> List[cst.SimpleStatementLine]:
        description: str = f"'''\n    {self.description}\n    '''"
        body = cst.Expr(value=cst.SimpleString(description))
        return [cst.SimpleStatementLine(body=[body])]

    @property
    def bases_class_CST(self) -> List[cst.Arg]:
        bases: List[cst.Arg] = []
        for base_class in self.base_classes:
            arg = cst.Arg(cst.Name(str(base_class)))
            bases.append(arg)
        return bases

    @property
    def class_attributes_CST(self) -> List[cst.SimpleStatementLine]:
        fields: List[cst.SimpleStatementLine] = []
        for attr in self.class_attributes:
            ann_assign = self.create_class_attr_CST(
                str(attr.get('name')), str(attr.get('value')), str(attr.get('type')))
            fields.append(ann_assign)
        return fields

    @property
    def instance_attributes_CST(self) -> List[cst.FunctionDef]:
        class_method_attrs: List[cst.SimpleStatementLine] = []
        method_name: cst.Name = cst.Name(self.class_name.lower() + '_method')

        for attr in self.instance_attributes:
            class_method_attrs.append(
                self.create_instance_attr_CST(str(attr.get('name')), str(attr.get('value')))
            )
        body = cst.IndentedBlock(body=class_method_attrs)
        return [cst.FunctionDef(
            name=method_name,
            params=cst.Parameters(params=[cst.Param(cst.Name('self'))]),
            body=body,
            decorators=[],
            returns=None
        )]

    @property
    def class_getter_methods_CST(self) -> List[cst.FunctionDef]:
        getters: List[cst.FunctionDef] = []
        for attr in self.instance_attributes:
            getters.append(self.create_getter_CST(str(attr.get('name')), str(attr.get('type'))))
        return getters

    @property
    def class_setter_methods_CST(self) -> List[cst.FunctionDef]:
        setters: List[cst.FunctionDef] = []
        for attr in self.instance_attributes:
            setters.append(self.create_setter_CST(str(attr.get('name')), str(attr.get('type'))))
        return setters

    @property
    def instance_methods_CST(self) -> List[cst.FunctionDef]:
        methods: List[cst.FunctionDef] = []
        for method in self.instance_methods:
            methods.append(self.create_instance_method_CST(
                method.get('name'),
                method.get('decorators'),
                method.get('arguments'),
                method.get('statements'),
                method.get('return_type')
            ))
        return methods

    def make_cst(self) -> cst.ClassDef:
        class_name = cst.Name(self.class_name)
        class_body = (
            self.class_description_CST + self.class_attributes_CST
            + self.instance_attributes_CST + self.class_getter_methods_CST
            + self.class_setter_methods_CST + self.instance_methods_CST
        )
        base_classes = self.bases_class_CST
        return cst.ClassDef(
            name=class_name,
            body=cst.IndentedBlock(body=class_body),
            bases=base_classes
        )

    def make_module(self, cst_node: cst.ClassDef) -> cst.Module:
        return cst.Module(body=[cst_node], header=self.default_header())

    def render_code(self, module: cst.Module, dest_path: Path) -> None:
        code = cst.Module([]).code_for_node(module)
        with open(dest_path, 'w') as file:
            file.write(code)
        return code


def main(data: dict, dest_path: Path) -> str:
    """
    :dest_path - this is a path that the generated *.py file should be saved.
    :data - this is a dictionary that has the class components
    for example,
    {
        "filename": "ex.py",
        "class": {
            "name": "test",
            "base_classes": [],
            "class_attributes": [{
                    "name": "a",
                    "type": int,
                    "value": 3
            }],
            "instance_attributes": [{
                "name": "key",
                "value": "val",
                "type": str
            }],
            "instance_methods": [{
                "decorators": [str],
                "name": "property",
                "arguments": [{
                        "name": "a",
                        "type": int
                }],
                "statements": ["a = 123"],
                "return_type": str
            }]
        }
    }
    """
    is_valid, err_msg = validation(data)
    if not is_valid:
        raise Exception(err_msg)
    if not os.path.exists(dest_path):
        raise Exception('The dest_path you provide does not exist.')
    dest_path = os.path.join(dest_path, data.get('filename'))

    generator: Generator = Generator(data)
    cst_node = generator.make_cst()
    module = generator.make_module(cst_node)
    code = generator.render_code(module, dest_path)
    return code
