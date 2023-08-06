#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2022/8/14 10:57
# @Author  : zbc@mail.ustc.edu.cn
# @File    : chemical_tagger.py
# @Software: PyCharm

from xml.dom.minidom import parseString
from xml.parsers.expat import ExpatError
from xml.dom.minidom import Document, Element, Node, Text

import requests


class ChemicalTagger:

    @classmethod
    def _get_all(cls, doc: (Document, Element), tag: str) -> [Element]:
        els = doc.getElementsByTagName(tag)
        return els

    @classmethod
    def _get_els_by_tag_and_attr(cls, doc: Element, tag: str, attr_name: str, attr_value: str):
        els = doc.getElementsByTagName(tag)
        res = []
        for el in els:
            if el.getAttribute(attr_name) == attr_value:
                res.append(el)
        return res

    @classmethod
    def _get_all_cms(cls, doc: (Document, Element)):
        cm_els = cls._get_all(doc, 'OSCARCM')
        return [cls._get_cm_name_smiles(cm_el) for cm_el in cm_els]

    @classmethod
    def _get_cm_name_smiles(cls, cm_el: Element):
        names = []
        for oscar_el in cls._get_all(cm_el, 'OSCAR-CM'):
            name = oscar_el.firstChild.nodeValue
            names.append(name)
        smiles = cm_el.getAttribute("smiles")
        return {'name': ' '.join(names), 'smiles': smiles}

    @classmethod
    def _el_to_texts(cls, el: (Element, Node), res: [] = None):
        res = [] if res is None else res
        for child_el in el.childNodes:
            if isinstance(child_el, Text):
                res.append(child_el.nodeValue)
            else:
                res = cls._el_to_texts(child_el, res)
        return res

    @classmethod
    def _text_to_dom(cls, text: str) -> Document:
        xml_str = requests.post("http://114.214.205.122:8088/nlpj", json={"text": text}).text
        try:
            dom = parseString(xml_str)
            return dom
        except ExpatError as e:
            raise ValueError(f"{e}\n\n"
                             f"text: {text}\n\n"
                             f"response: {xml_str}\n\n"
                             f"XML 格式错误，可能是sentence格式出错，或者114.214.205.122:8088/nlp服务出错")

    @classmethod
    def text_to_mols(cls, text):
        dom = cls._text_to_dom(text)
        return cls._get_all_cms(dom)

    @classmethod
    def tag_text(cls, text):
        return requests.post("http://114.214.205.122:8088/nlpj", json={"text": text}).text


if __name__ == "__main__":
    pass
