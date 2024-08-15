
Begin 08-14-2024

Ref: https://github.com/sanskrit-lexicon/GRA/issues/34
This directory:
cd /c/xampp/htdocs/sanskrit-lexicon/GRA/issues/issue34

# -------------------------------------------------------------
Start with a copy of csl-orig/v02/gra/gra.txt at commit
  f677a655c4876c7adf668df631317b449d5c2100

# change to csl-orig repository on local installation
cd /c/xampp/htdocs/cologne/csl-orig/
# generate temp_gra_0 .txt in this directory
  git show  f677a655c:v02/gra/gra.txt > /c/xampp/htdocs/sanskrit-lexicon/GRA/issues/issue34/temp_gra_0.txt
# return to this directory
cd /c/xampp/htdocs/sanskrit-lexicon/GRA/issues/issue34

--------------------------------------------------------
In this (temp_gra_0.txt) version:
* gra_hwextra.txt is computed from gra.txt
  * alternates are indicated in gra.txt by comma-delimited values
    of the '<k2>' attribute of the metaline
* alternate headwords are introduced into gra.xml using
  gra.txt and gra_hwextra.txt.

We are aiming to have the information about alternates within
additional entries to gra.txt. 

The main task here is to initialize a new gra.txt

--------------------------------------------------------
althws:  This code is from csl-orig/v02/gra.
cp -r /c/xampp/htdocs/cologne/csl-orig/v02/gra/althws .
cp /c/xampp/htdocs/cologne/csl-orig/v02/gra/gra_hwextra.txt .

althws/redo.sh recomputes gra_hwextra.txt from gra.txt

Then, in hw.py (csl-pywork repo), gra.txt and gra_hwextra.txt
are used to compute grahw.txt:
  python3 hw.py ../orig/gra.txt hwextra/gra_hwextra.txt grahw.txt

grahw.txt has items for the
additional headwords from gra_hwextra.  These extra items of
grahw.txt are used to make
- grahw2.txt  
   python3 hw2.py grahw.txt grahw2.txt
- grahw0.txt
   python3 hw0.py grahw.txt grahw0.txt
- gra.xml
  python3 make_xml.py ../orig/gra.txt grahw.txt gra.xml


--------------------------------------------------------
Code check.
compute temp_gra_hwextra.txt
althws/redo1.sh
--------------------------------------------------------
cp -r althws althws0
revise althws0 to compute temp_gra_0.xml
cd althws0
sh redo.sh
914 records written to temp_gra_hwextra.txt

diff temp_gra_hwextra.txt ../gra_hwextra.txt  | wc -l
# 0   The files are identical.

----------------------------------------------------
further compute temp_grahw.txt
cd althws0
cp /c/xampp/htdocs/cologne/gra/pywork/grahw.txt tempprev_grahw.txt
cp /c/xampp/htdocs/cologne/gra/pywork/hw.py .
cp /c/xampp/htdocs/cologne/gra/pywork/parseheadline.py .

cd althws0
python3 hw.py ../temp_gra_0.txt temp_gra_hwextra.txt temp_grahw.txt
914 extra headwords from temp_gra_hwextra.txt
BEGIN hw.py init_entries
89076 lines read from ../temp_gra_0.txt
11871 entries found
END hw.py init_entries
12785 lines written to temp_grahw.txt

diff tempprev_grahw.txt temp_grahw.txt | wc -l
#0  - files are the same

--------------------------------------------------------
recompute gra.xml

cd althws0
cp /c/xampp/htdocs/cologne/gra/pywork/gra.xml tempprev_gra.xml
cp /c/xampp/htdocs/cologne/gra/pywork/make_xml.py .
cp /c/xampp/htdocs/cologne/gra/pywork/hwparse.py .

python3 make_xml.py ../temp_gra_0.txt temp_grahw.txt temp_gra.xml 

diff tempprev_gra.xml temp_gra.xml | wc -l
# 0   the files are identical
--------------------------------------------------------

temp_gra_1.txt
This will be created using temp_gra_0.txt and multik2a.txt
It has new entry for each extra headword

Example:
<L>1078.1<pc>0116<k1>arvan<k2>2. arva, arvan, arvaRa<type>alt<LP>1078<k1P>arva
<L>1078.2<pc>0116<k1>arvaRa<k2>2. arva, arvan, arvaRa<type>alt<LP>1078<k1P>arva
;
new entries (in gra.txt)
<L>1078.1<pc>0116<k1>arvan<k2>2. arva, arvan, arvaRa
{{Lbody=1078}}
<LEND>
<L>1078.2<pc>0116<k1>arvaRa<k2>2. arva, arvan, arvaRa
{{Lbody=1078}}
<LEND>

python convert_lbody.py temp_gra_0.txt althws0/multik2a.txt temp_gra_1.txt
89076 lines read from temp_gra_0.txt
11871 entries found
1808 from althws0/multik2a.txt
12785 records written to temp_gra_1.txt

Note:
wc -l althws0/temp_grahw.txt
12785 althws0/temp_grahw.txt
Note 12785 is same as number of entries in temp_gra_1.txt.  Good!
--------------------------------------------------------
mkdir althws1

Generate a version of grahw.txt and gra.xml from temp_gra_1.txt
  This uses a revision of hw.py -- the same revision as for MW

cd althws1
cp ../althws0/parseheadline.py .  # used by hw.py
# use an 'empty' hwextra file
touch temp_gra_hwextra.txt

# in hw.py, in class Hwmeta
old: keysall_list = ['L','pc','k1','k2','h','e']
new: keysall_list = ['L','pc','k1','k2','h']

python3 hw.py ../temp_gra_1.txt temp_gra_hwextra.txt temp_grahw.txt
0 extra headwords from temp_gra_hwextra.txt
79894 lines read from ../temp_gra_1.txt
12785 entries found
12785 lines written to temp_grahw.txt

diff ../althws0/temp_grahw.txt temp_grahw.txt | wc -l
 These files are different, because the gra.txt versions differ in
 regard to lines outside the entries.
 


python3 make_xml.py ../temp_gra_1.txt temp_grahw.txt temp_gra.xml 

diff temp_gra.xml ../althws0/temp_gra.xml | wc -l
# 3616
Note 3616 / 4 = 904
Why the difference?

In the (current) althws0 version an entry for extra headword has
two fields:
1. '<alt>.*?</alt> '
  example: '<alt><s>akutrA</s> is an alternate of <s>akutra</s>.</alt> '
2. <hwtype.*?/>
  example: '<hwtype n="alt" ref="25"/>'

The alt field generates output in displays.
The hwtype field is informational.

Conclusion: This is not a material difference.

-----------
write a program to check this is the only diff
python compare_xml.py temp_gra.xml ../althws0/temp_gra.xml compare_xml.txt
12790 from temp_gra.xml
12790 from ../althws0/temp_gra.xml
compare: ndiff= 0

So, alt and hwtype are  the only differences.

--------------------------------------------------------
At this point, we have a good conversion in althws1.
Now, Move the changes to althws1/hw.py into production:
edit csl-pywork/v02/makotemplates/pywork/hw.py

Then install local version from temp_gra_1.txt

cd ../ # issue34
cp temp_gra_1.txt /c/xampp/htdocs/cologne/csl-orig/v02/gra/gra.txt
cd /c/xampp/htdocs/cologne/csl-pywork/v02
# grep 'gra ' redo_xampp_all.sh
sh generate_dict.sh gra  ../../gra
sh xmlchk_xampp.sh gra
# ok
cd /c/xampp/htdocs/sanskrit-lexicon/GRA/issues/issue34

#  check that the newly generated gra.xml agrees with the version in althws1
diff /c/xampp/htdocs/cologne/gra/pywork/gra.xml althws1/temp_gra.xml  | wc -l
# 0  IT DOES AGREE!
--------------------------------------------------------
upload this latest local version of displays to cologne server

cd /c/xampp/htdocs/sanskrit-lexicon/GRA/issues/issue34
cp /c/xampp/htdocs/cologne/gra/downloads/graweb1.zip temp_graweb1.zip

--------------------------------------------------------
In this version of gra.txt,  the homonyms are embedded in k2 field of metaline.


****************************************************************
