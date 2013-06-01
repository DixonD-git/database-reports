# -*- coding: utf-8 -*-
#!/usr/bin/env python2.7

# Copyright 2008-2013 bjweeks, MZMcBride, SQL, Legoktm, DixonD-git

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

report_name = u'Розірвані перенаправлення'

report_template = u'''
Розірвані перенаправлення; дані станом на <onlyinclude>{0}</onlyinclude>.

{{| class="wikitable sortable plainlinks" style="width:100%%; margin:auto;"
|- style="white-space:nowrap;"
! №
! Перенаправлення
! Перенаправляє на
{1}
|}}
'''

sqlQuery = '''
/* brokenredirects.py SLOW_OK */
SELECT
  p1.page_namespace,
  ns_name,
  p1.page_title,
  rd_title
FROM redirect AS rd
JOIN page p1
ON rd.rd_from = p1.page_id
JOIN toolserver.namespace
ON p1.page_namespace = ns_id
AND dbname = "{0}"
LEFT JOIN page AS p2
ON rd_namespace = p2.page_namespace
AND rd_title = p2.page_title
WHERE rd_namespace >= 0
AND p2.page_namespace IS NULL
ORDER BY p1.page_namespace ASC, p1.page_title ASC;
'''.format(settings.dbname)

site, db, cursor = common.prepareEnvironment()

cursor.execute(sqlQuery)

i = 1
output = []
for row in cursor.fetchall():
    ns_name = unicode(row[1], 'utf-8')
    page_title = unicode(row[2], 'utf-8')
    redirect_target = unicode(row[3], 'utf-8')
    page_namespace = row[0]
    if page_namespace == 6 or page_namespace == 14:
        page_title = u':{0}:{1}'.format(ns_name, page_title)
    elif ns_name > 0:
        page_title = u'{0}:{1}'.format(ns_name, page_title)
    else:
        page_title = u'{0}'.format(page_title)
    table_row = u'''|-
| {0}
| [[{1}]]
| [[:{2}]]'''.format(i, page_title,redirect_target)
    output.append(table_row)
    i += 1

common.finishReport(db, cursor, site, report_name, report_template, [output], __file__)