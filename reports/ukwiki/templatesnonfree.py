# -*- coding: utf-8 -*-
#!/usr/bin/env python2.7

# Copyright 2008-2013 bjweeks, MZMcBride, DixonD-git

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
        return u'Шаблони, що включають невільні файли'

    def get_preamble_template(self):
        return u'Шаблони, що включають невільні файли; дані станом на <onlyinclude>%s</onlyinclude>.'

    def get_table_columns(self):
        return [u'Шаблон', u'Невільних файлів']

    def get_table_rows(self, conn):
        cursor = conn.cursor()
        cursor.execute('''
        /* templatesnonfree.py SLOW_OK */
        SELECT
            p.page_namespace,
            CONVERT(p.page_title USING utf8),
            COUNT(*)
        FROM page AS p
        INNER JOIN imagelinks AS il
        ON il.il_from = p.page_id
        INNER JOIN page as f
        ON il.il_to = f.page_title
        INNER JOIN categorylinks AS cl
        ON cl.cl_from = f.page_id
        WHERE
            p.page_namespace = 10
            AND f.page_namespace = 6
            AND cl.cl_to = '%s'
        GROUP BY p.page_namespace, p.page_title
        ORDER BY COUNT(*) DESC;
        ''' % u'Невільні_файли'.encode('utf-8'))

        for page_namespace, page_title, count in cursor:
            page_title = u'[[%s]]' % self.make_page_title(page_namespace, page_title)
            yield [page_title, count]

        cursor.close()