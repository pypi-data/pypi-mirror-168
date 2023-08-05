from typing import Tuple, Union
from instancemanager import ArgsManager, LineObjContainer

INDENTATION_LEVEL = 4


def read_txt(path: str) -> list[str]:
    with open(path, "r") as f:
        lines: list[str] = [k.replace("\n", "") for k in f.readlines()]
    return lines


def to_tuple(content: str,
             indentation_level: int = INDENTATION_LEVEL,
             split_symbol: str = " ",
             remove_semi_colon: bool = False) \
        -> Tuple[int,
                 list[str],
                 ArgsManager]:
    """
    Returns a pair of elements: the level of indentation and the content
    :param content: str, the content to parse
    :param indentation_level: int, the indentation level
    :param split_symbol: str, the indentation level to split with
    :param remove_semi_colon: bool, whether semicolons should be removed
    :return: Tuple[int,
                  list[str],
                  OrderedDict[str, str]]
              The first element is the level of indentation
              The second element is the list of strings
              The third is the dict or params
    """
    strip = content.lstrip()
    content_modified = str(strip)  # Making a hardcopy
    # Calculating return content
    if remove_semi_colon:
        content_modified = content_modified.replace(";", "")
    return_args = None
    if "(" in content_modified and ")" in content_modified:
        # Contains params
        parameter_text: str
        temp_content: str
        content_modified, parameter_text = content_modified.split("(")

        parent_text = content_modified.split(" ")[-1]
        # last element of content gets replaced
        # Keep elements after ")"
        parameter_text, temp_content = parameter_text.split(")")
        if len(temp_content.strip()) > 0:
            raise ValueError(f"Found an element {temp_content.strip()} "
                             f"after instance in line {content}.")
        parameter_text = parameter_text.removesuffix(")")
        if "=" not in parameter_text:
            raise ValueError("Unexpected params found in line {}."
                             .format(strip))
        return_args = ArgsManager(content=parameter_text,
                                  parent=parent_text)
        # print(temp_content)
        # print(parameter_text)
    return (int((len(content) - len(strip))
                / indentation_level)), \
           content_modified.split(split_symbol), \
           return_args


def read_source(path: str):
    """Returns the list of objects with an indentation_level,
     a content, and args"""
    mylist = read_txt(path)
    previous_line_obj: Union[None] = None
    previous_indentation: int = 0
    list_lines: list[LineObjContainer] = []
    for elem in mylist:
        indentation_level: int
        content: list
        args: ArgsManager
        indentation_level, content, args = to_tuple(elem,
                                                    INDENTATION_LEVEL,
                                                    remove_semi_colon=True)
        myline = LineObjContainer(indentation_level=indentation_level,
                                  content=content,
                                  args=args)
        list_lines.append(myline)
    return list_lines
