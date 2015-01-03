# -*- coding: utf-8 -*-
#!/usr/bin/env python2.7

# Copyright 2015 DixonD-git

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

import reports


class report(reports.report):
    def get_title(self):
        return u'Файли, які є у Вікісховищі'

    def get_preamble_template(self):
        return u'Файли, які є у Вікісховищі; дані станом на <onlyinclude>%s</onlyinclude>.'

    def get_table_columns(self):
        return [u'Файл']

    def get_table_rows(self, conn):
        cursor = conn.cursor()
        cursor.execute('''
        /* duplicated_files.py SLOW_OK */
        SELECT
            CONVERT(u.img_name USING utf8)
        FROM ukwiki_p.image AS u
        INNER JOIN commonswiki_p.image AS c
        ON c.img_name=u.img_name AND c.img_size=u.img_size
        ORDER BY u.img_name;
        ''')

        for page_title in cursor:
            yield [u'[[:Файл:%s|%s]]' % (page_title, page_title),]


        cursor.close()