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

report_name = u'Шаблони, що мають найбільше включень'

report_template = u'''
Шаблони, що мають найбільше включень (не більше 2000 записів); дані станом на <onlyinclude>{0}</onlyinclude>.

{{| class="wikitable sortable" style="width:100%%; margin:auto;"
|- style="white-space:nowrap;"
! №
! Шаблон
! Використання
|-
{1}
|}}
'''

sqlQuery = '''
/* mosttransclusions.py SLOW_OK */
SELECT
  ns_name,
  tl_title,
  COUNT(*)
FROM templatelinks
JOIN toolserver.namespace
      ON dbname = "{0}"
      AND ns_id = tl_namespace
WHERE tl_namespace = 10
GROUP BY tl_title
ORDER BY COUNT(*) DESC
LIMIT 2000;
'''.format(settings.dbname)

site, db, cursor = common.prepareEnvironment()

cursor.execute(sqlQuery)

i = 1
output = []
for row in cursor.fetchall():
    tl_namespace = unicode(row[0], 'utf-8')
    tl_title = unicode(row[1], 'utf-8')
    tl_title = u'[[{0}:{1}|{2}]]'.format(tl_namespace, tl_title, tl_title)
    uses = row[2]
    table_row = u'''| {0}
| {1}
| {2}
|-'''.format(i, tl_title, uses)
    output.append(table_row)
    i += 1

common.finishReport(db, cursor, site, report_name, report_template, [output], __file__)