# -*- coding: utf-8 -*-
#!/usr/bin/env python2.7

# Copyright 2013 DixonD-git

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

import codecs
import datetime
import os
import oursql
import login
import wikipedia as pywikibot
import settings
import locale

def uploadSourceCode(fileName, reportTitle, site):
    with codecs.open(fileName, 'r', 'utf8') as f:
        sourceCode = f.read()

    sourceCode = u'== {0} ==\n<div style="overflow:auto;">\n<source lang="python">\n{1}\n</source>\n</div>'.format(
        fileName, sourceCode)

    reportSourcePage = pywikibot.Page(site = site, title = reportTitle + settings.sourcepage)
    reportSourcePage.put(sourceCode, comment = settings.editsourcesumm)


def getReportDate(cursor):
    cursor.execute(
        'SELECT UNIX_TIMESTAMP() - UNIX_TIMESTAMP(rc_timestamp) FROM recentchanges ORDER BY rc_timestamp DESC LIMIT 1;')
    rep_lag = cursor.fetchone()[0]
    current_of = (datetime.datetime.utcnow() - datetime.timedelta(seconds=rep_lag)).strftime('%H:%M, %d %B %Y (UTC)')
    return unicode(current_of, 'utf-8')


def uploadReport(site, report_title, report_text):
    report = pywikibot.Page(site=site, title=report_title)
    report.put(report_text, comment=settings.editsumm)


def getConnection():
    return oursql.connect(db=settings.dbname,
        host=settings.host,
        read_default_file=os.path.expanduser("~/.my.cnf"),
        charset=None,
        use_unicode=False)


def getSiteAndLogin():
    site = pywikibot.Site(code=settings.sitecode)
    login.LoginManager(username=settings.username, password=settings.password, site=site).login()
    return site


def finishReport(db, cursor, site, report_name, report_template, outputs, source_file):
    report_title = settings.rootpage + report_name

    current_of = getReportDate(cursor)
    outputs = (u'\n'.join(output) for output in outputs)
    report_text = report_template.format(current_of, *outputs)
    uploadReport(site, report_title, report_text)

    uploadSourceCode(source_file, report_title, site)

    cursor.close()
    db.close()


def prepareEnvironment():
    locale.setlocale(locale.LC_ALL, '')

    site = getSiteAndLogin()
    db = getConnection()
    cursor = db.cursor()

    return site, db, cursor