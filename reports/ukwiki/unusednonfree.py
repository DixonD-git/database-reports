# -*- coding: utf-8 -*-
#!/usr/bin/env python2.7

# Copyright 2010-2013 bjweeks, MZMcBride, DixonD-git

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import reports


class report(reports.report):
    def get_title(self):
        return u'Невільні файли, що не використовуються'

    def get_preamble_template(self):
        return u'Невільні файли, що не використовуються; дані станом на <onlyinclude>%s</onlyinclude>.'

    def get_table_columns(self):
        return [u'Файл']

    def get_table_rows(self, conn):
        cursor = conn.cursor()
        cursor.execute('''
        /* unusednonfree.py SLOW_OK */
        SELECT
            CONVERT(page_title USING utf8)
        FROM (SELECT
                page_title
              FROM page
              JOIN categorylinks
              ON cl_from = page_id
              WHERE cl_to = "%s"
              AND page_namespace = 6) AS pgtmp
        WHERE NOT EXISTS
          (SELECT 1
           FROM   imagelinks
           WHERE  pgtmp.page_title = il_to)
        ORDER BY page_title
        ''' % u'Невільні_файли'.encode('utf-8'))

        for page_title, in cursor:
            page_title = u'[[:Файл:%s|%s]]' % (page_title, page_title)
            yield [page_title]

        cursor.close()