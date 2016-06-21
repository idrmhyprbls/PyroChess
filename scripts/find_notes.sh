#!/bin/bash
# Find TODO statements

\find . -type f -regex '.*\.\(py\|sh\|txt\|md\|rst\|perl\|dat\|awk\|c\|cpp\|h\|hpp\)$' | \egrep -v '(^\.\/tmp|find_notes\.sh$|README\.md$)' | xargs \egrep -I --color=auto '\<(TODO|FIXME|XXX|REMOVEME|REVISIT|BUG|FEATURE)\>'
