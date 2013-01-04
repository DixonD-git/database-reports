# -*- coding: utf-8 -*-
#!/usr/bin/env python2.7

# Copyright 2009-2013 bjweeks, MZMcBride, DixonD-git

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

import settings
import common

report_name = u'Сторінки описів файлів без відповідного файлу'

report_template = u'''
Сторінки описів файлів без відповідного файлу; дані станом на <onlyinclude>{0}</onlyinclude>.

{{| class="wikitable sortable plainlinks" style="width:100%%; margin:auto;"
|- style="white-space:nowrap;"
! №
! Сторінка
|-
{1}
|}}
'''

sqlQuery = '''
/* filelessfilepages.py SLOW_OK */
SELECT
  ns_name,
  pg1.page_title
FROM page AS pg1
JOIN toolserver.namespace
ON dbname = "{0}"
AND pg1.page_namespace = ns_id
WHERE NOT EXISTS (SELECT
                    img_name
                  FROM image
                  WHERE img_name = pg1.page_title)
AND NOT EXISTS (SELECT
                  img_name
                FROM commonswiki_p.image
                WHERE img_name = CAST(pg1.page_title AS CHAR))
AND NOT EXISTS (SELECT
                  1
                FROM commonswiki_p.page AS pg2
                WHERE pg2.page_namespace = 6
                AND pg2.page_title = CAST(pg1.page_title AS CHAR)
                AND pg2.page_is_redirect = 1)
AND pg1.page_namespace = 6
AND pg1.page_is_redirect = 0;
'''.format(settings.dbname)

site, db, cursor = common.prepareEnvironment()

cursor.execute(sqlQuery)

i = 1
output = []
for row in cursor.fetchall():
    page_title = u'[[:{0}:{1}|]]'.format(unicode(row[0], 'utf-8'), unicode(row[1], 'utf-8'))
    table_row = u'''| {0}
| {1}
|-'''.format(i, page_title)
    output.append(table_row)
    i += 1

common.finishReport(db, cursor, site, report_name, report_template, output, __file__)