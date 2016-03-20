"""generate an article in markdown format from a correctly formatted xmind workbook"""
import xmind
import xmind.core.markerref
import xmind.core.sheet


IGNORE_SYMBOL_NAME = "symbol-wrong"


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
        text = current.getTitle()

        if IGNORE_SYMBOL_NAME not in markers:

            # style is based on depth
            # depth 0 : title of workbook, we ignore
            #       1  : section (abstract/intro/...)
            #       2  : paragraph
            #       3/+: phrase within paragraph
            begin_symbol = ""
            end_symbol = ""
            if current_level == 1:
                begin_symbol = "\n# "
            elif current_level == 2:
                begin_symbol = "\n***"
                end_symbol = "***"
            document.append("{0}{1}{2}".format(begin_symbol, text, end_symbol))

        # continue traversal
        children = current.getSubTopics()
        child_level = current_level
        if IGNORE_SYMBOL_NAME not in markers:
            child_level += 1
        if children is not None:
            for child in reversed(current.getSubTopics()):
                stack.append((child, child_level))
    return document
