#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from base import MyZotero


zot = MyZotero()


def strip_braces(field):
    updated_field = field.lstrip('{').rstrip('}')
    has_changed = updated_field != field
    if has_changed:
        print("Stripped braces from", field, "->", updated_field)
    return updated_field, has_changed


def lstrip_doi(field):
    updated_field = field.lstrip('http://dx.doi.org/')
    has_changed = updated_field != field
    if has_changed:
        print("Stripped http://dx.doi.org/ from", field, "->", updated_field)
    return updated_field, has_changed


def fix_braces(items, dry_run=True):
    for item in items:
        # If the number of keys is zero, it was a deleted entry, or
        # otherwise uninteresting.
        if len(item['meta'].keys()):
            data = item['data']
            doi_changed = False
            pages_changed = False
            if 'DOI' in data:
                item['data']['DOI'], doi_changed = strip_braces(data['DOI'])
                item['data']['DOI'], doi_changed_again = lstrip_doi(data['DOI'])
                doi_changed = doi_changed or doi_changed_again
            if 'pages' in data:
                item['data']['pages'], pages_changed = strip_braces(data['pages'])

            if doi_changed or pages_changed:
                print(item['data']['extra'])

            if not dry_run:
                zot.update_item(item)
    if dry_run:
        print("WARNING: just a dry run")


if __name__ == "__main__":
    thesis = zot.get_collection(
        #  "thesis"
        "paper_03_toy_model"
        # "paper_04_swe"
    )
    # Get everything
    items = zot.everything(zot.collection_items(thesis["key"]))
    fix_braces(items)
