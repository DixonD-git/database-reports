# -*- coding: utf-8 -*-
#!/usr/bin/env python2.7

# Copyright 2008-2014 bjweeks, MZMcBride, DixonD-git

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
        return u'Довгі сторінки обговорення'

    def get_preamble_template(self):
        return u'''Довгі сторінки обговорення; дані станом на <onlyinclude>%s</onlyinclude>.

Сторінки обговорення, довжина яких перевищує 140 000 байтів \
(не включаючи підсторінки і сторінки у користувацькому просторі)'''

    def get_table_columns(self):
        return [u'Сторінка', u'Довжина', u'Останнє редагування']

    def get_table_rows(self, conn):
        cursor = conn.cursor()
        cursor.execute('''
        /* longtalkpages.py SLOW_OK */
        SELECT
          page_namespace,
          CONVERT(page_title USING utf8),
          page_len,
          rev_timestamp
        FROM page
        JOIN revision
        ON rev_page = page_id
        WHERE page_len > 140000
        AND page_title NOT LIKE "%%/%%"
        AND page_namespace != 3
        AND page_namespace mod 2 != 0
        AND rev_timestamp = (SELECT
                               MAX(rev_timestamp)
                             FROM revision
                             WHERE rev_page = page_id)
        ORDER BY page_len DESC, page_namespace ASC;
        ''')

        for page_namespace, page_title, page_len, rev_timestamp in cursor:
            dbr_link = u'{{dbr link|1=%s}}' % self.make_page_title(page_namespace, page_title)
            yield [dbr_link, page_len, rev_timestamp]

        cursor.close()