#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""
    xmind.core.labels
    ~~~~~~~~~~~~~~~~
    :copyright:
    :license:
"""

__author__ = "axel.voitier@gmail.com <Axel Voitier>"

from . import const

from .mixin import TopicMixinElement


class LabelsElement(TopicMixinElement):
    TAG_NAME = const.TAG_LABELS

    def __init__(self, node=None, ownerTopic=None):
        super(LabelsElement, self).__init__(node, ownerTopic)


class LabelElement(TopicMixinElement):
    TAG_NAME = const.TAG_LABEL

    def __init__(self, node=None, ownerTopic=None):
        super(LabelElement, self).__init__(node, ownerTopic)
        
    def getLabel(self):
        return self.getTextContent()
        
    def setLabel(self, label_text):
        self.setTextContent(label_text)


def main():
    pass

if __name__ == '__main__':
    main()
