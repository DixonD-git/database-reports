# -*- coding: utf-8 -*-
#!/usr/bin/env python2.7

# Copyright 2008-2014 bjweeks, MZMcBride, SQL, Legoktm, DixonD-git

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
        return u'Розірвані перенаправлення'

    def get_preamble_template(self):
        return u'Розірвані перенаправлення; дані станом на <onlyinclude>%s</onlyinclude>.'

    def get_table_columns(self):
        return [u'Перенаправлення', u'Перенаправляє на']

    @staticmethod
    def __make_page_title(page_namespace, page_title):
        ns_name = '{{ns:%s}}' % page_namespace
        if page_namespace == 6 or page_namespace == 14:
            page_title = ':%s:%s' % (ns_name, page_title)
        elif page_namespace != 0:
            page_title = '%s:%s' % (ns_name, page_title)
        else:
            page_title = '%s' % page_title
        return '[[%s]]' % page_title

    def get_table_rows(self, conn):
        cursor = conn.cursor()
        cursor.execute('''
        /* brokenredirects.py SLOW_OK */
        SELECT
          p1.page_namespace,
          CONVERT(p1.page_title USING utf8),
          rd_namespace,
          CONVERT(rd_title USING utf8)
        FROM redirect AS rd
        JOIN page p1
        ON rd.rd_from = p1.page_id
        LEFT JOIN page AS p2
        ON rd_namespace = p2.page_namespace
        AND rd_title = p2.page_title
        WHERE rd_namespace >= 0
        AND p2.page_namespace IS NULL
        ORDER BY p1.page_namespace ASC;
        ''')

        for page1_namespace, page1_title, page2_namespace, page2_title in cursor:
            yield [self.__make_page_title(page1_namespace, page1_title),
                   self.__make_page_title(page2_namespace, page2_title)]


        cursor.close()