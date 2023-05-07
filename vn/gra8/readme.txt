
Add full '<chg>' markup to '<c n>X</c>'
-----------------------------------------------------------------
temporary display at localhost/sanskrit-lexicon/GRA/vn/tempgradisp/web/

cd /c/xampp/htdocs/sanskrit-lexicon/GRA/vn/
cp temp_gra_7.txt /c/xampp/htdocs/cologne/csl-orig/v02/gra/gra.txt
cd /c/xampp/htdocs/cologne/csl-pywork/v02
sh generate_dict.sh gra /c/xampp/htdocs/sanskrit-lexicon/GRA/vn/tempgradisp
# restore csl-orig
cd /c/xampp/htdocs/cologne/csl-orig/v02/gra/
git restore gra.txt
cd /c/xampp/htdocs/sanskrit-lexicon/GRA/vn/
-------------
At this point, temp_gra_7.txt is same as tempgradisp/orig/gra.
diff temp_gra_7.txt tempgradisp/orig/gra.7 | wc -l
# 0 (no diff)
---------------------------------------------
To remake the temporary display
- modify tempgradisp/orig/gra.txt
cd /c/xampp/htdocs/sanskrit-lexicon/GRA/vn/tempgradisp
sh redo.sh
--- action of redo.sh
cd tempgradisp/pywork
sh redo_hw.sh
sh redo_xml.sh
sh redo_postxml.sh
---
-----------------------------------------------------------------
Start with copy of temp_gra_7
cd /c/xampp/htdocs/sanskrit-lexicon/GRA/vn/gra8
cp ../temp_gra_7.txt temp_gra_8.txt

# to regenerate display
sh redo_disp.sh temp_gra_8.txt
-----------------------------------------------------------------
Use vn3_2.txt
cp ../orig/vn3_2.txt temp_vn3_2.txt

<chg type="chg" n="1" src="gra"><old>X</old><new>Y</new></chg>

modify basicadjust.php and basicdisplay.php


basicadjust
  $line = preg_replace_callback('|<chg(.*?)>(.*?)</chg>|',"BasicAdjust::chg_markup",$line);

<c 39a> <p>118 Ueberschrift: arvācīná    ::AB:: st. avācīná
 Requires no change in gra.txt. The error  is in a column heading,
 and column headings are not part of the gra.txt digitization.
 
python make_change8.py ../temp_gra_7.txt ../orig/vn3_2.txt temp_gra_8_prep.txt

check_d2: (2) <c 10> <p>22,28: á-joṣa, jóṣa    ::AB:: st. á-josa, jósa
check_d2: (2) <c 17> <p>34,11.10 v. u.: {%reingesinnt%}    ::AB:: st. {%untrügli
che%} u. s. w.
check_d2: (2) <c 22> <p>49,31.b v. u.: -ā́ṇaam    ::AB:: st. -āṇaam
check_d2: (0) <c 27> <p>68,16: annā-vṛ́dh    ::AB:: st. annā́-vṛdh
check_d2: (2) <c 49> <p>156,9.b v. u: -āṇi    ::AB:: st. āni
check_d2: (0) <c 50> <p>157,17: -ā́ṇi    ::AB:: st. -ā́ni
check_d2: (3) <c 63> <p>213,28.b v. u.: {106,1. 6}.    ::AB:: st. {106,1. 5}.
check_d2: (0) <c 64> <p>215,10 v. u.: indra-    ::AB:: st. índra-
check_d2: (0) <c 65> <p>216,20.21.a: {658,1—9}    ::AB:: st. {658,1. 9}
check_d2: (0) <c 147> <p>742,15: bṛ́haspátim    ::AB:: st. agním

=======
python diff_to_changes_dict_corr.py ../temp_gra_7.txt temp_gra_8_prep.txt temp_change_8_prep.txt
264 changes written to temp_change_8_prep.txt
--------------------------------
cp ../orig/vn3_2.txt temp_vn3_2.txt
SOME MANUAL EDITING OF temp_vn3_2.txt

? interpretation of
c 17  (u.s.w.)
c 20  (u.s.w.)
c 31  
c 39a  heading not part of digitization of body
c 52 a-syandamāna  -?
c 58 ', ā́'  ?
<c 61> does {362,1. 7} link to 362,1?

--------------------------------
cp temp_change_8_prep.txt temp_change_gra_8a.txt
# manually edit temp_change_gra_8a.txt.
# in gra8,
# apply temp_change_gra_8a.txt to ../temp_gra_7.txt to get temp_gra_8a.txt
python ../updateByLine.py ../temp_gra_7.txt temp_change_gra_8a.txt temp_gra_8a.txt

86245 lines read from ../temp_gra_7.txt
86245 records written to temp_gra_8a.txt
288 change transactions from temp_change_gra_8a.txt
288 of type new

sh redo_disp.sh temp_gra_8a.txt
  # confirms xml is well-formed.  validity check remains.
-----------------------------------------------------------------
Grassman deletions
-----------------------------------------------------------------
in gra8,
cp temp_gra_8a.txt temp_gra_8b_prep.txt

# Manually edit temp_gra_8b_prep.txt,
#  adding markup for the 93 <d N> items of temp_vn3_2.txt

temp_vn3_2 questions:
<d 275>  bis = until.
d 276: two lines
<d 279>  <p>86,28—31: *  (should it be 28-30?) aBiSvasa
<d 291> <p>160,2 v. u. bis {161,4}: *  CANNOT FIND
vn correction:
 old: <d 316> <p>380,6—4.b v. u.: nas bis nas)
 new: <d 316> <p>380,16—14.b v. u.: nas bis nas)

<d 321> <p>473,5.b v. u.:4  better treated as a chg. {879,4. 5.}
<d 330> <p>631,26.a v. u.:5   {105,3. 5. 16} => {105,3.16} <d>5.</d>

---------------------------------------------------------------------
<chg type="del" n="1" src="gra"><old>X</old></chg>


python diff_to_changes_dict_corr.py temp_gra_8a.txt temp_gra_8b_prep.txt temp_change_8b_prep.txt
96 changes written to temp_change_8b_prep.txt

cp temp_change_8b_prep.txt temp_change_gra_8b.txt
# manually edit temp_change_gra_8b.txt.
# in gra8,
# apply temp_change_gra_8b.txt to temp_gra_8a.txt to get temp_gra_8b.txt
python ../updateByLine.py temp_gra_8a.txt temp_change_gra_8b.txt temp_gra_8b.txt
99 of type new
# remake displays, as a way to check that xml is well-formed.
sh redo_disp.sh	temp_gra_8b.txt
---------------------------------------------------------------
Add lines from vn to temp_gra_8.
First, save a copy of edited temp_vn3_2.txt
cp temp_vn3_2.txt ../orig/vn3_3.txt

Prepare vn (a and c) for inclusion in gra.txt.

cp temp_vn3_2.txt vn4.txt
edit vn4.txt
 1. ' *::AB:: *' -> ' '
 2. '<p>' -> ''
 3. '^<c \(.*?\)> \(.*\)$' -> \2 <info vn="chg \1 gra"/>
 4. '^<d \(.*?\)> \(.*\)$' -> \2 <info vn="del \1 gra"/>
 5. {161,4} -> 161,4  (at del 291)
-------------
create vn5.txt
(a) get metaline from temp_gra_8b by matching <info vn="X N gra"/>
(b) generate L-number sequentially, starting at L=11000
    (last metaline in temp_gra_8b is <L>10777<pc>1684<k1>hvf<k2>hvf, hru

python make_meta_vn_cd.py temp_gra_8b.txt vn4.txt vn5.txt


-------------
temp_gra_8.txt
join temp_gra_8b and vn5
cat temp_gra_8b.txt vn5.txt > temp_gra_8.txt
------------
sh redo_disp.sh temp_gra_8.txt


-----------------------------------------------------------------
DONE: Add pdfpages for VN to Grassman images
 Images are there (locally)
 update webtc/pdffiles.txt
NOTE:  This may be just a problem with relocation

DONE:  display 'del' items  (basicadjust)

DONE: <info vn="chg 5 gra">  in display (basicadjust)

-----------------------------------------------------------------
Additions
orig/vn3add.txt
lines from [Page1749] to the end  (2166 lines)

Objective is to add meta-lines, then append to temp_gra_8.txt.
cp ../orig/vn3add.txt vn3add_1.txt

Make changes to vn3add_1.txt so that headword matching can be done.

The additions in vn3add_1 are partially identified <a X>.
 Lines so starting are the 'start' of an addition-entry.
 The last one ins <a 635> sthavira.
   The lines after this line are another topic (somehow related to Aufrecht Rg Veda).
 Lines starting with '<h>' will not be part of entries.

Except for this last <a 635>, the scope of an entry in vn3add_1 extends
 from <a X> up to the blank line preceding the next <a Y>.
 Some entries have blank lines (before that 'last') blank line.
To simplify the identification of the scope of entries,  I edit vn3add_1.txt
  to remove the intermediate blank lines.
  With this change, an entry consists of an <a X> line up to the next blank line.
To simplify parsing of headwords,
  :</b> -> </b>:
Some spelling changes:
 n1 -> ṅ  (7)
Some entries are missed (have no <a x>) in vn3add_1.txt.
  66 matches for "<a [0-9]+[abc]>" in buffer: vn3add_1.txt
  Add a temporary <a N[abc]> -- may renumber later.  


python make_meta_vn_a.py temp_gra_8.txt vn3add_1.txt vn6_add.txt
  
¦

\(<a .*?> <p><b>[^<]*</b>:\) → x\1

 Now 458 lines start with 'x<a'
  and 242 start with '<a' (+ 458 242)

109 matches for "<a [^>]*> <p><b>.*?,</b>"

\(<a .*?> <p><b>[^<]*\),</b> → x\1</b>,   108 changes

 Now 566 lines start with 'x<a'
  and 134 start with '<a' (+ 566 134) = 

\(<a [^>]*> <p>[0-9]+\. <b>[^<]*</b>\) → x\1¦   (43 changes)

\(<a [^>]*> <p>[0-9]+\. <b>[^<]*</b>\) → x\1¦  (15 changes)

\(<a [^>]*> <p>[*]<b>[^<]*\),</b> → x\1</b>¦,  (22 changes)

\(<a [^>]*> <p><b>[^<]*</b>\)  → x\1¦  (45 changes)

Add ¦ to remaining 9 ^<a

</b>): -> </b>)¦:  (15 changes)
</b>: -> </b>¦:  (713 changes)

 ¥ -> 〰  (55 changes)
,</b>¦ -> </b>¦, (20 changes approx.)
 a3 -> á (2 changes)
 ŕ → ṛ́ (50 changes)
-----------------------------------------------------------------
editing vn3add_1.txt at line 493  (corrections with ¦)
-----------------------------------------------------------------
There are now 701 'headword' lines:The '<p>' is not needed here
    ^\(<a [0-9]+[a-d]?>\) <p> → \1

610 matches for "<a [0-9]+[abcd]?> <b>[^<]+</b>¦" in buffer: vn3add_1.txt
  <a 15> <b>aṅgá</b>¦:
  
44 matches for "<a [^<]+> [1-9]\. <b>[^<]+</b>¦" in buffer: vn3add_1.txt
  <a 53b> 2. <b>ándhas</b>¦: 

16 matches for "<a [0-9]+[a-d]> [(]<b>" in buffer: vn3add_1.txt
  <a 13a> (<b>ághnya</b)¦: -ā 603,4.

--------------------------------------
python make_meta_vn_a.py temp_gra_8.txt vn3add_1.txt vn6_add.txt
87732 lines read from temp_gra_8.txt
11151 entries found
701 records written to vn6_add.txt
-----------------------------------
vn6_add_1.txt
Some adjustments. Results aim to be compatible with gra.txt

 
38 matches for "NEW " in buffer: vn6_add.txt
  additions with a new headword (not in gra.txt) identified by an
  asterisk in vn. <a 5> *<b>a-karmán</b>

python vn6_add_1.py vn6_add.txt vn6_add_1.txt
-----------------------------------
temp_gra_9.txt
cat temp_gra_8.txt vn6_add_1.txt > temp_gra_9.txt
# to regenerate display
sh redo_disp.sh temp_gra_9.txt

Problem with use of <lang> and <gk> in Andhrabharati's revisions included in
gra_8.txt.

-----------------------------------
prepare Cologne version of display:  work/gra9/
sh prepare_upload.sh gra9
#
cologne display url:
  https://sanskrit-lexicon.uni-koeln.de/work/gra-dev/gra9/web/
