#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from base import MyZotero, strip_braces, lstrip_doi


zot = MyZotero()


thesis = zot.get_collection(
    #  "thesis"
    "paper_03_toy_model"
    # "paper_04_swe"
)
# Get everything
items = zot.everything(zot.collection_items(thesis["key"]))
apply_filters = {
    "DOI": (strip_braces, lstrip_doi),
    "pages": (lstrip_doi,)
}
zot.fix(items, apply_filters, dry_run=True)
