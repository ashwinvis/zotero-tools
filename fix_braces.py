#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from contextlib import suppress
from base import MyZotero


zot = MyZotero()


def strip_braces(field):
    updated_field = field.lstrip('{').rstrip('}')
    has_changed = updated_field != field
    if has_changed:
        print("Stripped braces from", field)
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
            if 'pages' in data:
                item['data']['pages'], pages_changed = strip_braces(data['pages'])

            if doi_changed or pages_changed:
                with suppress(KeyError):
                    print(item['data']['DOI'])

                with suppress(KeyError):
                    print(item['data']['pages'])

                print(item['data']['extra'])

            if not dry_run:
                zot.update_item(item)


if __name__ == "__main__":
    thesis = zot.get_collection("thesis")
    # Get everything
    items = zot.everything(zot.collection_items(thesis["key"]))
    fix_braces(items)
