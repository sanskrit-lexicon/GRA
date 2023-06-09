echo "BEGIN redo_xml.sh"
echo "construct gra.xml..."
python3 make_xml.py ../orig/gra.txt grahw.txt gra.xml # > redoxml_log.txt
echo "xmllint on gra.xml..."
xmllint --noout --valid gra.xml
echo "gra.sqlite..."
#  construct things that depend on xxx.xml
sh redo_postxml.sh
echo "END redo_xml.sh"
