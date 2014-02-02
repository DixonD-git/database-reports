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
        return u'Шаблони, що мають найбільше включень'

    def get_preamble_template(self):
        return u'Шаблони, що мають найбільше включень (не більше 2000 записів); ' \
               u'дані станом на <onlyinclude>%s</onlyinclude>.'

    def get_table_columns(self):
        return [u'Шаблон', u'Використання']

    def get_table_rows(self, conn):
        cursor = conn.cursor()
        cursor.execute('''
        /* mosttransclusions.py SLOW_OK */
        SELECT
          CONVERT(tl_title USING utf8),
          COUNT(*)
        FROM templatelinks
        WHERE tl_namespace = 10
        GROUP BY tl_title
        ORDER BY COUNT(*) DESC
        LIMIT 2000;
        ''')

        for tl_title, count in cursor:
            tl_title = u'[[Шаблон:%s|%s]]' % (tl_title, tl_title)
            yield [tl_title, count]

        cursor.close()