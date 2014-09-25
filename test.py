#! /usr/bin/env env
# -*- coding: utf-8 -

import os
import sys
import glob

manga = "/tenkuu_shinpan/"
path = os.getcwd() + manga
roots = []
for root, dirs, files in os.walk(path):
	roots.append(root)
    # print root

roots = roots[1:]
roots.sort()

for root in roots:
	print root
