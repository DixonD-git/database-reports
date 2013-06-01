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

import common
import settings

report_name = u'Великі невільні файли'
non_free_media_category = u'Невільні_файли'

report_template = u'''
Невільні файли, розмір яких більший, ніж 999999 байтів; дані станом на <onlyinclude>{0}</onlyinclude>.

{{| class="wikitable sortable plainlinks" style="width:100%%; margin:auto;"
|- style="white-space:nowrap;"
! №
! Файл
! Розмір
|-
{1}
|}}
'''

sqlQuery = '''
/* largenonfree.py SLOW_OK */
SELECT
  ns_name,
  page_title,
  img_size
FROM page
JOIN toolserver.namespace
ON dbname = "{0}"
AND page_namespace = ns_id
JOIN image
ON img_name = page_title
JOIN categorylinks
ON cl_from = page_id
WHERE page_namespace = 6
AND cl_to = "{1}"
AND img_size > 999999
ORDER BY img_size DESC;
'''.format(settings.dbname, non_free_media_category.encode('utf-8'))

site, db, cursor = common.prepareEnvironment()

cursor.execute(sqlQuery)

i = 1
output = []
for row in cursor.fetchall():
    ns_name = unicode(row[0], 'utf-8')
    page_title = unicode(row[1], 'utf-8')
    full_page_title = u'[[:{0}:{1}|{2}]]'.format(ns_name, page_title, page_title)
    img_size = row[2]
    table_row = u'''| {0}
| {1}
| {2}
|-'''.format(i, full_page_title, img_size)
    output.append(table_row)
    i += 1

common.finishReport(db, cursor, site, report_name, report_template, [output], __file__)
