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

import settings
import common

report_name = u'Довгі сторінки'

report_template = u'''
Довгі сторінки; дані станом на <onlyinclude>{0}</onlyinclude>.

== Визначені сторінки обговорення ==
Сторінки обговорення, довжина яких перевищує 140 000 байтів \
(не включаючи підсторінки і сторінки у користувацькому просторі).

{{| class="wikitable sortable plainlinks" style="width:100%%; margin:auto;"
|- style="white-space:nowrap;"
! №
! Сторінка
! Довжина
! Останнє редагування
|-
{1}
|}}

== Всі сторінки ==
Всі сторінки, довжина яких перевищує 500 000 байтів.

{{| class="wikitable sortable plainlinks" style="width:100%%; margin:auto;"
|- style="white-space:nowrap;"
! №
! Сторінка
! Довжина
! Останнє редагування
|-
{2}
|}}
'''

sqlQuery1 = '''
/* longpages.py SLOW_OK */
SELECT
  ns_name,
  page_title,
  page_len,
  rev_timestamp
FROM page
JOIN toolserver.namespace
ON page_namespace = ns_id
AND dbname = "{}"
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
ORDER BY page_len, page_namespace ASC;
'''.format(settings.dbname)

sqlQuery2 = '''
/* longpages.py SLOW_OK */
SELECT
  ns_name,
  page_title,
  page_len,
  rev_timestamp
FROM page
JOIN toolserver.namespace
ON page_namespace = ns_id
AND dbname = "{}"
JOIN revision
ON rev_page = page_id
WHERE page_len > 500000
AND rev_timestamp = (SELECT
                       MAX(rev_timestamp)
                     FROM revision
                     WHERE rev_page = page_id)
ORDER BY page_len, page_namespace ASC;
'''.format(settings.dbname)

site, db, cursor = common.prepareEnvironment()

cursor.execute(sqlQuery1)

i = 1
output1 = []
for row in cursor.fetchall():
    ns_name = unicode(row[0], 'utf-8')
    page_title = unicode(row[1], 'utf-8')
    if ns_name:
        page_title = u'{{{{dbr link|1={0}:{1}}}}}'.format(ns_name, page_title)
    else:
        page_title = u'{{{{dbr link|1={0}}}}}'.format(page_title)
    page_len = row[2]
    rev_timestamp = row[3]
    table_row = u'''| {0}
| {1}
| {2}
| {3}
|-'''.format(i, page_title, page_len, rev_timestamp)
    output1.append(table_row)
    i += 1

cursor.execute(sqlQuery2)

i = 1
output2 = []
for row in cursor.fetchall():
    ns_name = unicode(row[0], 'utf-8')
    page_title = unicode(row[1], 'utf-8')
    if ns_name:
        page_title = u'{{{{dbr link|1={0}:{1}}}}}'.format(ns_name, page_title)
    else:
        page_title = u'{{{{dbr link|1={0}}}}}'.format(page_title)
    page_len = row[2]
    rev_timestamp = row[3]
    table_row = u'''| {0}
| {1}
| {2}
| {3}
|-'''.format(i, page_title, page_len, rev_timestamp)
    output2.append(table_row)
    i += 1

common.finishReport(db, cursor, site, report_name, report_template, [output1, output2], __file__)