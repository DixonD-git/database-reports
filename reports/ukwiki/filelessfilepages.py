# -*- coding: utf-8 -*-
#!/usr/bin/env python2.7

# Copyright 2009-2015 bjweeks, MZMcBride, DixonD-git

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
        return u'Сторінки описів файлів без відповідного файлу'

    def get_preamble_template(self):
        return u'Сторінки описів файлів без відповідного файлу; дані станом на <onlyinclude>%s</onlyinclude>.'

    def get_table_columns(self):
        return [u'Файл']

    def get_table_rows(self, conn):
        cursor = conn.cursor()
        cursor.execute('''
        /* filelessfilepages.py SLOW_OK */
        SELECT
          pg1.page_title
        FROM page AS pg1
        WHERE pg1.page_title NOT IN (
            SELECT
                img_name
            FROM image
            WHERE img_name = pg1.page_title)
        AND pg1.page_title NOT IN (
            SELECT
                img_name
            FROM commonswiki_p.image
            WHERE img_name = pg1.page_title)
        AND pg1.page_namespace = 6
        AND pg1.page_is_redirect = 0
        ORDER BY pg1.page_title;
        ''')

        for page_title, in cursor:
            page_title = u'[[:Файл:%s|%s]]' % (page_title, page_title)
            yield [page_title]

        cursor.close()
