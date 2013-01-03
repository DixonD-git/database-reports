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
import wikipedia as pywikibot
import settings

def uploadSourceCode(fileName, reportTitle, site):
    with codecs.open(fileName, 'r', 'utf8') as f:
        sourceCode = f.read()

    sourceCode = u'== {0} ==\n<div style="overflow:auto;">\n<source lang="python">\n{1}\n</source>\n</div>'.format(
        fileName, sourceCode)

    reportSourcePage = pywikibot.Page(site = site, title = reportTitle + settings.sourcepage)
    reportSourcePage.put(sourceCode, comment = settings.editsourcesumm)
