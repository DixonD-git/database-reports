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

import common
import settings

report_name = u'Сторінки, що включають значну кількість невільних файлів'

non_free_media_category = u'Невільні_файли'

report_template = u'''
Сторінки, що включаються більше, ніж 6 невільних файлів; дані станом на <onlyinclude>{0}</onlyinclude>.

{{| class="wikitable sortable plainlinks" style="width:100%%; margin:auto;"
|- style="white-space:nowrap;"
! №
! Сторінка
! Невільні файли
|-
{1}
|}}
'''

sqlQuery = '''
/* pageslotnonfree.py SLOW_OK */
SELECT
  imgtmp.page_namespace,
  imgtmp.ns_name,
  imgtmp.page_title,
  COUNT(cl_to)
FROM page AS pg1
JOIN categorylinks
ON cl_from = pg1.page_id
JOIN (SELECT
        pg2.page_namespace,
        ns_name,
        pg2.page_title,
        il_to
      FROM page AS pg2
      JOIN toolserver.namespace
      ON dbname = "{0}"
      AND pg2.page_namespace = ns_id
      JOIN imagelinks
      ON il_from = page_id) AS imgtmp
ON il_to = pg1.page_title
WHERE pg1.page_namespace = 6
AND cl_to = '{1}'
GROUP BY imgtmp.page_namespace, imgtmp.page_title
HAVING COUNT(cl_to) > 6
ORDER BY COUNT(cl_to) DESC;
'''.format(settings.dbname, non_free_media_category.encode('utf-8'))

site, db, cursor = common.prepareEnvironment()

cursor.execute(sqlQuery)

i = 1
output = []
for row in cursor.fetchall():
    page_namespace = row[0]
    ns_name = unicode(row[1], 'utf-8')
    page_title = unicode(row[2], 'utf-8')
    count = row[3]
    if page_namespace == 6 or page_namespace == 14:
        page_title = u'[[:{0}:{1}]]'.format(ns_name, page_title)
    elif page_namespace == 0:
        page_title = u'[[{0}]]'.format(page_title)
    else:
        page_title = u'[[{0}:{1}]]'.format(ns_name, page_title)
    table_row = u'''| {0}
| {1}
| {2}
|-'''.format(i, page_title, count)
    output.append(table_row)
    i += 1

common.finishReport(db, cursor, site, report_name, report_template, [output], __file__)