""" Script for blog."""

from statics.page import Page
from statics import element

__all__ = ["blog", "Entry", "Entries"]


class Entry(Page):
    """ Blog entry."""

    def get_context(self):
        context = super(Entry, self).get_context()
        context["entry"] = self
        return context


class Entries(element.TemplatedElementMixin, element.ContentElement):
    """ Blog entries."""

    def __init__(self, name, entries, site, template, children=None):
        element.ContentElement.__init__(self, name, children=children)
        self.entries = entries
        self.site = site
        self.template = template

    def get_context(self):
        return {"site": self.site, "entries": self.entries}


def blog(site, config, item):
    """ Produce element for each blog entry with paginated entries list and
    atom feed."""
    entries_template = site.templates.get_template(config["entries_template"])
    entry_template = site.templates.get_template(config["entry_template"])
    entries = list(reversed(item.values()))
    entries_element = Entries(item.name, entries, site, entries_template)
    for entry_item in entries:
        entry_element = Entry(entry_item, entry_template)
        entries_element[entry_item.name] = entry_element
    return entries_element
