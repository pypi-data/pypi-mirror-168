def wrap_text(node, tail, wrapper, start_pos=None, end_pos=None):
    """Wrap the text (or tail if tail is True) of a node in wrapper (a callable).
    Optionally, start_pos and end_pos specify the substring of the node's text (or tail)
    to be wrapped. The wrapper callable will be called with the text being wrapped.
    """
    if tail:
        text = node.tail or ""
        start_pos = start_pos or 0
        end_pos = len(text) if end_pos is None else end_pos
        wrapped = wrapper(text[start_pos:end_pos])

        node.addnext(wrapped)
        node.tail = text[:start_pos]
        wrapped.tail = text[end_pos:]
    else:
        text = node.text or ""
        start_pos = start_pos or 0
        end_pos = len(text) if end_pos is None else end_pos
        wrapped = wrapper(text[start_pos:end_pos])

        node.text = text[:start_pos]
        node.insert(0, wrapped)
        wrapped.tail = text[end_pos:]

    return wrapped


def unwrap_element(elem):
    """ Unwrap text and children inside elem, making them children
    of elem's parents.

    Example:
        <p>text <term>a <b>term</b></term> with a tail</p>

        unwrapping <term> produces:

        <p>text a <b>term</b> with a tail</p>
    """
    parent = elem.getparent()
    prev = elem.getprevious()

    if prev is not None:
        # elem is not the first child of its parent
        prev.tail = (prev.tail or '') + (elem.text or '')
        index = parent.index(elem)
        last = None
        for child in elem.iterchildren(reversed=True):
            if last is None:
                last = child
            parent.insert(index, child)

        if last is None:
            last = prev
        last.tail = (last.tail or '') + (elem.tail or '')

    else:
        # elem is first child of its parent
        parent.text = (parent.text or '') + (elem.text or '')
        last = None
        for child in elem.iterchildren(reversed=True):
            if last is None:
                last = child
            parent.insert(0, child)

        if last is not None:
            last.tail = (last.tail or '') + (elem.tail or '')
        else:
            parent.text = (parent.text or '') + (elem.tail or '')

    parent.remove(elem)


def merge_adjacent(e, nxt):
    """ Combine two adjacent elements into the first one.
    """
    kids = list(e)
    if kids:
        # put text at end of last child
        kids[-1].tail = (kids[-1].tail or '') + (nxt.text or '')
    else:
        # append text to ours
        e.text = (e.text or '') + (nxt.text or '')
    e.tail = nxt.tail
    for kid in nxt.iterchildren():
        e.append(kid)
    nxt.getparent().remove(nxt)
