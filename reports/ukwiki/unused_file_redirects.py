# -*- coding: utf-8 -*-
#!/usr/bin/env python2.7
 
# Copyright 2009-2013 bjweeks, MZMcBride, svick, DixonD-git
 
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
        return u'Перенаправлення файлів, що не використовуються'

    def get_preamble_template(self):
        return u'Перенаправлення файлів, на які є щонайбільше одне посилання; дані станом на <onlyinclude>%s</onlyinclude>.'

    def get_table_columns(self):
        return [u'Сторінка', u'Використань файлу', u'Посилань на файл']

    def get_table_rows(self, conn):
        cursor = conn.cursor()
        cursor.execute('''
        /* unused_file_redirects.py SLOW_OK */
        SELECT
            page_namespace,
            page_title,
            (SELECT COUNT(*)
            FROM imagelinks
            WHERE il_to = page_title) AS imagelinks,
            (SELECT COUNT(*)
            FROM pagelinks
            WHERE pl_title = page_title) AS links
        FROM page
        WHERE
            page_namespace = 6
            AND page_is_redirect = 1
        HAVING imagelinks + links <= 1;
        ''')

        for page_namespace, page_title, count1, count2 in cursor:
            page_title = u'[[%s]]' % self.make_page_title(page_namespace, page_title)
            yield [page_title, count1, count2]

        cursor.close()