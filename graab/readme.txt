Work on integrating Andhrabharati's version of Grassman (with vn) into
CDSL display system.

----
initial version, as provided by Andhrabharati at
   https://github.com/sanskrit-lexicon/GRA/issues/29
cp ~/Downloads/gra/gra_.CSL._.AB.-8b.chg.corrections.done.txt temp_graab_0.txt
----
# temp_graab_1.txt  Change so constructed xml is well-formed.

cp temp_graab_0.txt temp_graab_1.txt
python diff_to_changes_dict.py temp_graab_0.txt temp_graab_1.txt change_1.txt
27 changes written to change_1.txt


----------------------------------------------------------------------
# Revise basicadjust.php in csl-websanlexicon, using gra9
cp /c/xampp/htdocs/sanskrit-lexicon/GRA/vn/gra-dev/web/webtc/basicadjust.php /c/xampp/htdocs/cologne/csl-websanlexicon/v02/makotemplates/web/webtc/

and also basicdisplay.php

cp /c/xampp/htdocs/sanskrit-lexicon/GRA/vn/gra-dev/web/webtc/basicdisplay.php /c/xampp/htdocs/cologne/csl-websanlexicon/v02/makotemplates/web/webtc/


# sh redo.sh and examine

diff /c/xampp/htdocs/sanskrit-lexicon/GRA/vn/gra-dev/web/webtc/basicadjust.php dev1/web/webtc/basicadjust.php

diff /c/xampp/htdocs/sanskrit-lexicon/GRA/vn/gra-dev/web/webtc/basicdisplay.php dev1/web/webtc/basicdisplay.php

diff /c/xampp/htdocs/sanskrit-lexicon/GRA/vn/gra-dev/pywork/make_xml.py dev1/pywork/make_xml.py 
----------------------------------------------------------------------
temp_vn_ab.txt: AB versions of VN material
mkdir vn_ab
See vn_ab/readme.txt for creation of temp_vn_ab.txt
TODO: [Note: In my final version, couple of metaline data got chang# add the vn part to the body part.
cat temp_graab_1.txt vn_ab/temp_vn_ab.txt > temp_graab_2.txt

----------------------------------------------------------------------
# change redo.sh to now use temp_graab_2.txt with results in dev2

----------------------------------------------------------------------
Compare meta-lines of temp_gra9.txt to metalines of temp_graab_2.txt
See meta_compare/readme.txt and readme_diff.txt

----------------------------------------------------------------------
cp temp_graab_2.txt temp_graab_3.txt 
CORRECTIONS to graab_3
see graab/change_3.txt (3 changes)
----------------------------------------------------------------------
See readme_printchange_notes.txt for notes on
PRINT CHANGES TO BE REGISTERD in csl-corrections/dictionaries/gra/gra_printchange.txt
----------------------------------------------------------------------
now redo.sh uses temp_graab_3.txt for dev3. (06-11-2023)
----------------------------------------------------------------------

