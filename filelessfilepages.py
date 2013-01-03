# -*- coding: utf-8 -*-
#!/usr/bin/env python2.7

# Copyright 2009 bjweeks, MZMcBride, DixonD-git

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

import os
import datetime
import oursql
import settings
import wikipedia as pywikibot
import login
import locale
import common

locale.setlocale(locale.LC_ALL, '')

report_title = settings.rootpage + u'Сторінки описів файлів без відповідного файлу'

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

site = pywikibot.Site(code = settings.sitecode)
login.LoginManager(username=settings.username, password=settings.password, site = site).login()

db = oursql.connect(db=settings.dbname,
    host=settings.host,
    read_default_file=os.path.expanduser("~/.my.cnf"),
    charset=None,
    use_unicode=False)

cursor = db.cursor()
cursor.execute('''
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
'''.format(settings.dbname))

i = 1
output = []
for row in cursor.fetchall():
    page_title = u'[[:{0}:{1}|]]'.format(unicode(row[0], 'utf-8'), unicode(row[1], 'utf-8'))
    table_row = u'''| {0}
| {1}
|-'''.format(i, page_title)
    output.append(table_row)
    i += 1

cursor.execute('SELECT UNIX_TIMESTAMP() - UNIX_TIMESTAMP(rc_timestamp) FROM recentchanges ORDER BY rc_timestamp DESC LIMIT 1;')
rep_lag = cursor.fetchone()[0]
current_of = (datetime.datetime.utcnow() - datetime.timedelta(seconds=rep_lag)).strftime('%H:%M, %d %B %Y (UTC)')

report = pywikibot.Page(site = site, title = report_title)
report_text = report_template.format(unicode(current_of, 'utf-8'), u'\n'.join(output))
report.put(report_text, comment = settings.editsumm)

common.uploadSourceCode(__file__, report_title, site)

cursor.close()
db.close()
