#!/usr/bin/env python
"""generate an article in markdown format from a correctly formatted xmind workbook"""

import xmind
import xmind.core.markerref
import xmind.core.sheet
import argparse

# style is based on markers
#       1  : section (abstract/intro/...)
#       2  : paragraph
#       3/+: phrase within paragraph

MARKERS_TO_SYMBOLS = {"priority-1": lambda x: "{}{}{}".format("\n# ", x, ""),
                      "priority-2": lambda x: "{}{}{}".format("\n## ", x, ""),
                      "priority-3": lambda x: "{}{}{}".format("\n***", x, "***"),
                      "symbol-exclam":lambda x: "{}".format(x)}
MARKER_WRONG = "symbol-wrong"


def dump_markdown(sheet):
    assert isinstance(sheet, xmind.core.sheet.SheetElement)

    stack = [(sheet.getRootTopic(), 0)]
    document = []

    while len(stack) > 0:
        # extract the data from the node
        current, current_level = stack.pop()

        # add the text to the document, depending on the current context
        # markers encode behavior
        raw_markers = current.getMarkers()
        markers = []
        if raw_markers is not None:
            markers = [marker.getMarkerId().name for marker in current.getMarkers()]
        text =  clean_non_unicode(current.getTitle())
        
        if MARKER_WRONG not in markers:
            if len(markers) == 1:
                document.append(MARKERS_TO_SYMBOLS[markers[0]](text))

        # continue traversal
        children = current.getSubTopics()
        child_level = current_level
        if MARKER_WRONG not in markers:
            child_level += 1
        if children is not None:
            for child in reversed(current.getSubTopics()):
                stack.append((child, child_level))
    return document

def clean_non_unicode(string):
    return ''.join([i if ord(i) < 128 else ' ' for i in string])

def write_to_file(document, output_file):
    with open(output_file, "w") as handle:
        for line in document:
            handle.write("{}\n".format(line))
    return 




if __name__ == "__main__":
    PARSER = argparse.ArgumentParser("matrix symmetrizer for RNAdistance")
    PARSER.add_argument("-i", "--input_file", type=str, help="rna distance matrix file")
    PARSER.add_argument("-o", "--output", type=str, help="output file")
    ARGS = PARSER.parse_args()
    
    IN = ARGS.input_file
    write_to_file(dump_markdown(xmind.load(IN).getPrimarySheet()), ARGS.output)
