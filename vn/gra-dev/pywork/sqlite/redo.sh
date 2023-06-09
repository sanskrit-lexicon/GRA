sqlitedb="gra.sqlite"
xml="../gra.xml"
echo "remaking $sqlitedb from $xml with python..."
python3 sqlite.py $xml $sqlitedb
echo "moving $sqlitedb to web/sqlite/"
mv gra.sqlite ../../web/sqlite/
