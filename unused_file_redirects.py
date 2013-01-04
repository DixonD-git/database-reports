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

import settings
import common

report_name = u'Перенаправлення файлів, що не використовуються'
 
report_template = u'''
Перенаправлення файлів, на які є щонайбільше одне посилання; дані станом на <onlyinclude>{0}</onlyinclude>.
 
{{| class="wikitable sortable plainlinks"
|-
! №
! Сторінка
! Використання файлу
! Посилання
|-
{1}
|}}
'''

sqlQuery = '''
/* unused_file_redirects.py */
SELECT ns_name, pg1.page_title,
  (SELECT COUNT(*)
  FROM imagelinks
  WHERE il_to = page_title) AS imagelinks,
  (SELECT COUNT(*)
  FROM pagelinks
  WHERE pl_namespace = 6
    AND pl_title = page_title) AS links
FROM page AS pg1
JOIN toolserver.namespace
ON dbname = "{0}"
AND pg1.page_namespace = ns_id
WHERE pg1.page_namespace = 6
  AND pg1.page_is_redirect = 1
HAVING imagelinks + links <= 1
'''.format(settings.dbname)

site, db, cursor = common.prepareEnvironment()

cursor.execute(sqlQuery)
 
i = 1
output = []
for row in cursor.fetchall():
    page_title = u'<span class="plainlinks">[{{{{fullurl:{0}:{1}|redirect=no}}}} {2}]</span>'.format(
        unicode(row[0], 'utf-8'), unicode(row[1], 'utf-8'), unicode(row[1], 'utf-8'))
    imageLinks = row[2]
    links = row[3]
    table_row = u'''| {0}
| {1}
| {2}
| {3}
|-'''.format(i, page_title, imageLinks, links)
    output.append(table_row)
    i += 1

common.finishReport(db, cursor, site, report_name, report_template, [output], __file__)
