""" Script for blog."""

from datetime import datetime

from feedformatter import Feed as FeedGenerator

from statics.pages import Page
from statics import element

__all__ = ["blog", "Entry", "Entries"]


class Entry(Page):
    """ Blog entry."""

    def __init__(self, item, site, template, children=None):
        Page.__init__(self, item, site, template, children=children)
        if not "title" in self.metadata:
            raise ValueError("Item '%s' for blog entry does not provide"
                             "'title' as metadata." % item.location)
        self.published_date = datetime.strptime(
            self.item.name[:10], "%Y-%m-%d")

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


class Feed(element.ContentElement):

    def __init__(self, name, entries, site, children=None):
        element.ContentElement.__init__(self, name, extension="xml",
                                        children=children)
        self.entries = entries
        self.site = site

    def render(self):
        feed = FeedGenerator()
        feed.feed["title"] = self.site["main"]["title"]
        feed.feed["author"] = self.site["main"]["author"]
        feed.feed["link"] = self.site["main"]["url"]

        for entry in self.entries:
            feed.items.append({
                "title": entry.title,
                "link": "%s%s" % (feed.feed["link"], entry.item.location),
                "pubDate": entry.published_date.timetuple(),
                "guid": entry.item.location,
            })

        return feed.format_atom_string()


def blog(site, config, item):
    """ Produce element for each blog entry with paginated entries list and
    atom feed."""
    entries = list(reversed(item.values()))
    if not entries:
        return element.Element(item.name)


    entries_template = site.templates.get_template(config["entries_template"])
    entry_template = site.templates.get_template(config["entry_template"])

    children = [Entry(e, site, entry_template) for e in entries]
    entries_element = Entries(
        item.name, children, site, entries_template, children=children)
    entries_element["feed"] = Feed("feed", children, site)
    return entries_element
