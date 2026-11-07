# 
# 0. copy xxxheader.xml from pywork to web
cp graheader.xml ../web/
# 1. Redo web/xxx.sqlite
cd sqlite || exit 1
sh redo.sh
cd ../ # back in pywork
# 2. redo db (query_dump) for advanced search
cd webtc2 || exit 1
sh redo.sh
cd ../ # back to pywork
# For applicable dictionaries, update other web/sqlite databases
# abbreviations
 cd graab || exit 1
 sh redo.sh
 cd ../ # back to pywork
# literary source.
# two extra links dbs for mw
