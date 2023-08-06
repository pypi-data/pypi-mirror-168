#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2022/9/21 16:24
# @Author  : zhangbc0315@outlook.com
# @File    : fast_xml.py
# @Software: PyCharm

from xml.dom.minidom import parseString
from xml.parsers.expat import ExpatError
from xml.dom.minidom import Document, Element, Node, Text


class FastXML:

    @classmethod
    def parse_string(cls, xml_str: str):
        return parseString(xml_str)

    @classmethod
    def _el_to_texts(cls, el: (Element, Node), res: [] = None) -> [str]:
        res = [] if res is None else res
        for child_el in el.childNodes:
            if isinstance(child_el, Text):
                res.append(child_el.nodeValue)
            else:
                res = cls._el_to_texts(child_el, res)
        return res

    @classmethod
    def _is_leaf_node(cls, node: Node):
        return isinstance(node.firstChild, Text)

    @classmethod
    def _get_leaf_nodes(cls, xml, non_leaf_tags: [str]):
        for child_el in xml.childNodes:
            if cls._is_leaf_node(child_el):
                yield child_el
            elif child_el.tagName in non_leaf_tags:
                yield child_el
            else:
                for leaf_node in cls._get_leaf_nodes(child_el, non_leaf_tags):
                    yield leaf_node

    @classmethod
    def get_token_tag_pairs_and_attrs(cls, xml, non_leaf_tags: [str], attrs: [str]):
        token_tag_pairs = []
        res_attrs = {}
        for attr in attrs:
            res_attrs[attr] = []
        for leaf_node in cls._get_leaf_nodes(xml, non_leaf_tags):
            texts = cls._el_to_texts(leaf_node)
            token_tag_pairs.append((leaf_node.tagName, ' '.join(texts)))
            for attr in attrs:
                res_attrs[attr].append(leaf_node.getAttribute(attr))
        return token_tag_pairs, res_attrs

    @classmethod
    def xml_to_json(cls, xml):
        res = {}
        for child_el in xml.childNodes:
            if isinstance(child_el, Text):
                return child_el.nodeValue
            else:
                res[child_el.tagName] = cls.xml_to_json(child_el)
        return res


if __name__ == "__main__":
    x = FastXML.parse_string("<root><A><B>b</B><C>c</C></A><A1 upper='A1'>a1</A1></root>")
    print(FastXML.xml_to_json(x))
    print(FastXML.get_token_tag_pairs_and_attrs(x, ['A'], ['upper']))
