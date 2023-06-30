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
TODO: [Note: In my final version, couple of metaline data got change
 # add the vn part to the body part.
# cat temp_graab_1.txt vn_ab/temp_vn_ab.txt > temp_graab_2.txt
# revision (for st. and v.u. abbreviations in the 'chg' section.
cat temp_graab_1.txt vn_ab/temp_vn_ab_a.txt > temp_graab_2.txt

----------------------------------------------------------------------
# change redo.sh to now use temp_graab_2.txt with results in dev2

----------------------------------------------------------------------
Compare meta-lines of temp_gra9.txt to metalines of temp_graab_2.txt
See meta_compare/readme.txt and readme_diff.txt

----------------------------------------------------------------------
CORRECTIONS 
see graab/change_3.txt (5 changes)
python updateByLine.py temp_graab_2.txt change_3.txt temp_graab_3.txt
89186 lines read from temp_graab_2.txt
89186 records written to temp_graab_3.txt
5 change transactions from change_3.txt
One further change put into change_3.txt, namely
  <lang n="German">germ.</lang> ->  <lang>germ.</lang>
  
----------------------------------------------------------------------
See readme_printchange_notes.txt for notes on
PRINT CHANGES TO BE REGISTERD in csl-corrections/dictionaries/gra/gra_printchange.txt
----------------------------------------------------------------------
now redo.sh uses temp_graab_3.txt for dev3. (06-11-2023)
----------------------------------------------------------------------
modify dtd for gra
python /c/xampp/htdocs/cologne/xmlvalidate.py dev3/pywork/gra.xml dev3/pywork/gra.dtd
See readme_dtd.txt for revisions.

----------------------------------------------------------------------
temp_graab_4.txt : tooltip markup changes
abbrevs/graab_input.txt  : revised abbreviation tooltip file for displays
see abbrevs/readme.txt

cp abbrevs/graab_input.txt /c/xampp/htdocs/cologne/csl-pywork/v02/distinctfiles/gra/pywork/graab/graab_input.txt

TODO?: abbrevs  Ref https://github.com/sanskrit-lexicon/GRA/issues/27#issuecomment-1594202101
  s.u.d.W


revise csl-websanlexicon/.../basicadjust.py to treat
  <lang> and <pe> tags just like <ab> tags.
change redo to use temp_graab_4

sh redo.sh
python /c/xampp/htdocs/cologne/xmlvalidate.py dev4/pywork/gra.xml dev4/pywork/gra.dtd

----------------------------------------------------------------------
6-16-2023  
<ls> markup
see litsrc directory. see litsrc/readme.txt.
------ 1.  Remove 'local' abbrevs.
 temp_graab_5a.txt 
 
python diff_to_changes_dict.py temp_graab_4.txt temp_graab_5a.txt change_5a.txt 
35 changes written to change_5a.txt

------ 2. AV links, part 1
 temp_graab_5b.txt
python diff_to_changes_dict.py temp_graab_5a.txt temp_graab_5b.txt change_5b.txt
188 changes written to change_5b.txt

------ 3. AV links, part 2
 temp_graab_5c.txt
python diff_to_changes_dict.py temp_graab_5b.txt temp_graab_5c.txt change_5c.txt
 5 changes written to change_5c.txt
------
cp temp_graab_5c.txt temp_graab_5.txt

----------------------------------------------------------------------


change redo.sh to use version 5. Update .gitignore
sh redo.sh
python /c/xampp/htdocs/cologne/xmlvalidate.py dev5/pywork/gra.xml dev5/pywork/gra.dtd

----------------------------------------------------------------------
----------------------------------------------------------------------
----------------------------------------------------------------------
TODO: handle 

46. AB hw correction (? Complicated.  Currently these two don't show)
 12319 guhya  (addition)
  3002 guhia  (and guhya)
11470c11489
< <L>12319<k1>guhia
---
> <L>12319<k1>guhya
--------------------------------
47. AB hw correction (? Complicated.  Currently these two don't show)
11733c11752
< <L>12582<k1>vIrya
---
> <L>12582<k1>vIria
--------------------------------------------------------------
TODO: "1." has to be expanded as '1sten/ersten', not as '1ten/ersten'.
Example: <pe n="1ten/ersten">1.</pe>
--------------------------------------------------------------
(f.:feminium) -- local should be changed to (f.:femininum) -- global; it is a manual typing error on my part.Just seen your separation files for global and local abbr.s
31 matches for "feminium" in buffer: temp_graab_3.txt
--------------------------------------------------------------
TODO: 〉 to ).
--------------------------------------------------------------
TODO: 3 cases of !√  e.g. {@(!√jaṅgahe)@}

--------------------------------------------------------------
TODO: {x,y. z}  -> {x,y} {x,z}  in ADD section. ?
--------------------------------------------------------------
TODO:  (last step) Have precisely one blank line between <LEND> and <L>
--------------------------------------------------------------
See readme_todo_graab_5.txt for collection of items which I should
review.  These are drawn from issue29, starting from the
comments following the upload of temp_graab_5.

--------------------------------------------------------------
**************************************************************
BEGIN WORK with Andhrabharati's revision of temp_graab_5,
REF: https://github.com/sanskrit-lexicon/GRA/issues/31#issuecomment-1601350550
download temp_graab_6.txt  and temp_graab_6.AB.txt
  (only difference is use in 6.AB. of special characters for
   'details' of ls refs for ls other than AV and RV.  888 of these.
For convenience, rename
unzip ~/Downloads/gra/temp_graab_6.AB.zip
  inflating: temp_graab_6(AB).txt
mv temp_graab_6(AB).txt temp_graab_6_bracket.txt
uses square brackets 〔I,283〕

unzip ~/Downloads/gra/temp_graab_6.zip
  inflating: temp_graab_6.txt
mv temp_graab_6.txt temp_graab_6_curly.txt
uses only curly brackets

I will do work starting with the 'bracket'.

**************************************************************
change_6.txt:
Ref: 
Last minute changes to temp_graab_6_bracket.txt

-------
temp_graab_6.txt
python updateByLine.py temp_graab_6_bracket.txt change_6.txt temp_graab_6.txt
8 change transactions from change_6.txt
--------------------------------------
TODO: What about '%%X%%' markup?
56 matches in 28 lines for "%%" in buffer: temp_graab_6.txt
Ref: https://github.com/sanskrit-lexicon/GRA/issues/31#issuecomment-1601996268
--------------------------------------
change to dtd. Allow 'ab' as attribute of 'ls' element'
see readme_dtd.txt
-------------
change redo.sh to use version 6. Update .gitignore
sh redo.sh
python /c/xampp/htdocs/cologne/xmlvalidate.py dev6/pywork/gra.xml dev6/pywork/gra.dtd
-------------
**************************************************************
in litsrc1 directory,
- construct temp_graab_7a,b,c,d  (using change_7a,b,c,d)
  
- revise /c/xampp/htdocs/cologne/csl-pywork/v02/distinctfiles/gra/pywork/graauth/tooltip.txt

cp temp_graab_7e.txt temp_graab_7.txt

Revise redo.sh to use version 7
Add dev7 to .gitignore
Generate dev7: sh redo.sh

Check xml validity of dev7
python /c/xampp/htdocs/cologne/xmlvalidate.py dev7/pywork/gra.xml dev7/pywork/gra.dtd
-- ok!
**************************************************************
begin 06-25-2023
abbrevs1 directory
Begin with graab/temp_graab_7e.txt
make change_7f.txt and graab/temp_graab_7f.txt
cp temp_graab_7f.txt  temp_graab_7.txt
install new global abbreviation file for GRA in csl-pywork
sh redo.sh
**************************************************************
06-26-2023
litsrc2 directory
Markup for links to RV.
Change markup for 'non-standard' RV links to standard form {a,b}.
**************************************************************
06-27-2023 (begin)
mischg directory
miscellaneous changes
python updateByLine.py temp_graab_8.txt change_9a.txt temp_graab_9a.txt
38 lines changed.

temp_graab_9.txt

sh redo.sh #version 9
python /c/xampp/htdocs/cologne/xmlvalidate.py dev9/pywork/gra.xml dev9/pywork/gra.dtd
-------------------------------------------------------------
althws directory 
a few changes
change_9b.txt and temp_graab_9b.txt
cp temp_graab_9b.txt temp_graab_9.txt
generate gra_hwextra.txt  (916 alternate headwords).
sh redo.sh
-------------------------------------------------------------
meta2 directory
Revision to csl-orig/v02/gra/gra-meta2.txt
cp /c/xampp/htdocs/cologne/csl-orig/v02/gra/gra-meta2.txt gra-meta2_0.txt


-------------------------------------------------------------
-------------------------------------------------------------
