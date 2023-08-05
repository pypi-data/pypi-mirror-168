import json
from typing import Union
from collections import OrderedDict


class ArgsManager:
    def __init__(self,
                 content: str,
                 parent: Union[None, str] = None):
        self.content: OrderedDict[str, str] = OrderedDict()
        if content.count(",") + 1 != content.count("="):
            raise ValueError("Expected to find the same number"
                             " of \",\"  plus one {} symbols as \"=\" {} "
                             "in string {}."
            .format(
                content.count(",") + 1,
                content.count("="),
                content))
        content_list = content.split(",")
        for args in content_list:
            # print(args)
            key, value = args.split("=")
            key = key.replace(" ", "")
            value = value.replace(" ", "")
            self.content[key] = value
        self.parent = parent

    def __repr__(self):
        return json.dumps(self.content)


class LineObjContainer:
    def __init__(self,
                 indentation_level: int,
                 content: list,
                 args: ArgsManager
                 ):
        self.indentation_level: int = indentation_level
        self.content: list = content
        self.args: ArgsManager = args

    def __repr__(self):
        joined_content = "|".join(self.content)
        str_return: str = \
            f"Indentation: {self.indentation_level}\n " \
            f"Content: {joined_content}\n " \
            f"Args:{self.args}"
        return str_return
