#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright: error.d
# Date  : 2013-12-31
# Create by: error.d<error.d@gmail.com>
#

import sys
import json

def usage():
    print "usage: %s bookmarks html_bookmarks" % sys.argv[0]

class Bookmark:
    def __init__(self):
        self._json_bookmark = None
        self._html_bookmark = None
        self._level = 1
    
    def to_html_url_process(self, url_obj):
        self._level += 1
        print 'process', '\t'* self._level, 'url name: %s id: %s'% (url_obj['name'], url_obj['id'])
        self._html_bookmark += " " * self._level + '<DT><A HREF="%s">%s</A>\n' % (url_obj['url'], url_obj['name'])
        self._level -= 1

    def to_html_folder_process(self, folder_obj):
        self._level += 1
        print 'process', '\t' * self._level, 'folder name: %s id: %s' % (folder_obj['name'], folder_obj['id'])
        self._html_bookmark += " " * self._level + "<DT><H3>%s</H3>\n" % folder_obj['name']
        self._html_bookmark += " " * self._level + "<DL><p>\n"
        self.to_html_children_process(folder_obj['children'])
        self._html_bookmark += " " * self._level + "</DL><p>\n"
        self._level -= 1

    def to_html_children_process(self, childrens):
        if not childrens:
            return

        for children in childrens:
            if children['type'] == 'folder':
                self.to_html_folder_process(children)
            elif children['type'] == 'url':
                self.to_html_url_process(children)

    def to_html_bookmark_process(self, obj):
        for bookmark_name, bookmarks in obj.items():
            if bookmark_name in ('meta_info'):
                continue
            self.to_html_children_process(bookmarks['children'])

    def to_html(self):
        if not self._json_bookmark:
            return

        self._html_bookmark = """<!DOCTYPE NETSCAPE-Bookmark-file-1>
<!-- This is an automatically generated file.
     It will be read and overwritten.
     DO NOT EDIT! -->
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
<TITLE>Bookmarks</TITLE>
<H1>Bookmarks</H1>
<DL><p>
<DT><H3 PERSONAL_TOOLBAR_FOLDER="true">Bookmarks Bar</H3>
"""

        if 'roots' not in self._json_bookmark:
            return

        roots = self._json_bookmark['roots']
        self.to_html_bookmark_process(roots)
        
        self._html_bookmark += """
</DL><p>"""

    def save_html_bookmark(self, html_filepath):
        with open(html_filepath, 'w') as html_file:
            html_file.write(self._html_bookmark.encode('utf8'))

    def open_json_bookmark(self, json_filepath):
        with open(json_filepath, 'r') as jb_file:
            jb = ''.join(jb_file.readlines())
            self._json_bookmark = json.loads(jb)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        usage()
        sys.exit(0)
    bookmark = Bookmark()
    bookmark.open_json_bookmark(sys.argv[1])
    bookmark.to_html()
    bookmark.save_html_bookmark(sys.argv[2])


