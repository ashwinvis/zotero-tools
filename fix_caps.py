#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from base import MyZotero


zot = MyZotero()


def fix_caps(items):
    for item in items:
        if "correctcase" in item['meta'] and item['meta']['correctcase']:
            continue
        else:
            item['meta']['correctcase'] = 1
            title = item['data']['title']
            s = title.split()
            capscount = 0
            for ss in s:  # Loop once to figure out how many words have capital letters in them
                preservecap = any([l for l in ss if l.isupper()])
                if preservecap:
                    capscount += 1
            # Heavy capitalization means too much capitalization (probably). Keeps sporadic capitalized stuff (like Arabidopsis) from being demoted if possible
            if capscount > len(s) / 4:
                for i, ss in enumerate(s):
                    # I want to preserve the capitalization if any char after the first is capitalized.
                    preservecap = any([l for l in ss[1:] if l.isupper()])
                    if not preservecap:
                        # This makes sure I capitalize words that follow
                        if i and s[i-1][-1] == ':':
                            s[i] = ss.capitalize()
                        else:
                            s[i] = ss.lower()
            newtitle = " ".join(s)
            if capscount == len(s):  # Everything was capitalized!
                newtitle = newtitle.lower()
                newtitle = newtitle.capitalize()
            item['data']['title'] = newtitle
            zot.update_item(item)
