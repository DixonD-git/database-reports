#!/usr/bin/env python2.5
 
# Copyright 2009-2010 bjweeks, MZMcBride, svick
 
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
 
import datetime
import MySQLdb
import wikitools
import settings
 
report_title = settings.rootpage + 'Talk subpages with redirect parent'
 
report_template = u'''
This page lists first 1000 talk subpages (exclusing user talk subpages) whose parent talk page is a redirect. Data as of <onlyinclude>%s</onlyinclude>.

{| class="wikitable sortable plainlinks"
|-
! No.
! Page
|-
%s
|}
'''
 
wiki = wikitools.Wiki(settings.apiurl)
wiki.login(settings.username, settings.password)
 
conn = MySQLdb.connect(host=settings.host, db=settings.dbname, read_default_file='~/.my.cnf')
cursor = conn.cursor()
cursor.execute('''
/* subtalks_of_redirects.py */
select ns_name, sub.page_title
from page sub
join page parent
  on sub.page_namespace = parent.page_namespace
  and parent.page_title = substring_index(sub.page_title, '/', 1)
join toolserver.namespacename
  on ns_id = sub.page_namespace
where sub.page_namespace % 2 = 1
and sub.page_namespace != 3
and sub.page_title like '%/%'
and sub.page_is_redirect = 0
and parent.page_is_redirect = 1
and dbname = 'enwiki_p'
order by sub.page_namespace, sub.page_title
limit 1000
''')
 
i = 1
pages = []
for row in cursor.fetchall():
    page_title = '[[%s:%s]]' % (unicode(row[0], 'utf-8'), unicode(row[1].replace('_', ' '), 'utf-8'))
    table_row = u'''| %d
| %s
|-''' % (i, page_title)
    pages.append(table_row)
    i += 1

cursor.execute('SELECT UNIX_TIMESTAMP() - UNIX_TIMESTAMP(rc_timestamp) FROM recentchanges ORDER BY rc_timestamp DESC LIMIT 1;')
rep_lag = cursor.fetchone()[0]
current_of = (datetime.datetime.utcnow() - datetime.timedelta(seconds=rep_lag)).strftime('%H:%M, %d %B %Y (UTC)')

 
report = wikitools.Page(wiki, report_title)
report_text = report_template % (current_of, '\n'.join(pages))
report_text = report_text.encode('utf-8')
report.edit(report_text, summary=settings.editsumm, bot=1)
 
cursor.close()
conn.close()
