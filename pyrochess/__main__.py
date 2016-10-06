#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import

if __name__ == '__main__':
    from pyrochess import config
    from pyrochess.cli import main
    config.Settings.imported = False
    main()
