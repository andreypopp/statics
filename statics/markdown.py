""" Item with markdown content."""

from __future__ import absolute_import

import markdown

from statics.item import ContentItem

__all__ = ["MarkdownItem"]


def exclude_one_element_values(d):
    ret = {}
    for k, v in d.items():
        if isinstance(v, list) and len(v) == 1:
            ret[k] = v[0]
        else:
            ret[k] = v
    return ret


class MarkdownItem(ContentItem):
    """ Item with markdown content."""

    def __init__(self, *args, **kw):
        super(MarkdownItem, self).__init__(*args, **kw)

    def get_parser(self):
        return markdown.Markdown(extensions=["meta"])

    def metadata(self):
        parser = self.get_parser()
        raw_content = super(MarkdownItem, self).content()
        parser.convert(raw_content)
        return exclude_one_element_values(parser.Meta)

    def content(self):
        parser = self.get_parser()
        raw_content = super(MarkdownItem, self).content()
        content = parser.convert(raw_content)
        return content
