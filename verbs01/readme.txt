
Analysis of gra verbs and upasargas, revised
This work was done in a temporary subdirectory (temp_verbs) of csl-orig/v02/gra/.

The shell script redo.sh reruns 5 python programs, from mwverb.py to preverb1.py.


* mwverbs
python mwverb.py mw ../../mw/mw.txt mwverbs.txt
#copy from v02/mw/temp_verbs
#cp ../../mw/temp_verbs/verb.txt mwverbs.txt
each line has 5 fields, colon delimited:
 k1
 L
 verb category: genuinroot, root, pre,gati,nom
 cps:  classes and/or padas. comma-separated string
 parse:  for pre and gati,  shows x+y+z  parsing prefixes and root

* mwverbs1.txt
python mwverbs1.py mwverbs.txt mwverbs1.txt
Merge records with same key (headword)
Also  use 'verb' for categories root, genuineroot, nom
and 'preverb' for categories pre, gati.
Format:
 5 fields, ':' separated
 1. mw headword
 2. MW Lnums, '&' separated
 3. category (verb or preverb)
 4. class-pada list, ',' separated
 5. parse. Empty for 'verb' category. For preverb category U1+U2+...+root

* gra_verb_filter.

python gra_verb_filter.py ../gra.txt  gra_verb_exclude.txt gra_verb_include.txt gra_verb_filter.txt

The first line of each entry is examined for several EXCLUSION patterns.
This leaves 995 non-excluded records as verb candidates.
A few additional records (gra_verb_exclude.txt) are excluded.
A few additional records (gra_verb_include.txt) are included.

Total 907 entries identified as verbs.

Format of file gra_verb_filter.txt:
;; Case 0001: L=11, k1=aMh, k2=aMh, code=V
;; Case 0002: L=40, k1=akz, k2=akz, code=V


* gra_verb_filter_map
python gra_verb_filter_map.py gra_verb_filter.txt mwverbs1.txt gra_verb_filter_map.txt

Get correspondences between gra verb spellings and
 - gra verb spellings
 - mw verb spellings

Format of gra_verb_filter_map.txt:
 Adds a field mw=xxx to each line of gra_verb_filter.txt,
indicating the MW root believed to correspond to the GRA root.
For example, aMSay in GRA is believed to correspond to aMS in MW.
;; Case 0001: L=11, k1=aMh, k2=aMh, code=V, mw=aMh
;; Case 0002: L=40, k1=akz, k2=akz, code=V, mw=akz

In 24 cases, no correspondence could be found. These use 'mw=?'. For example:
;; Case 0004: L=130, k1=aNkUy, k2=aNkUy, code=V, mw=?


* preverb0
python preverb0.py ../gra.txt gra_verb_filter_map.txt gra_upasarga_map.txt gra_preverb0.txt 
NOTE 1: code modified from md/temp_verbs01/preverb0.py
NOTE 2: In the first run, 'prelim(filedbg,dhatus)' wrote possible upasarga
      information for each verb; and at the end, wrote a preliminary mapping
      from the possible upasarga text snippets to SLP1-spelled upasargas.
      See preverb0_dbg.txt.
Note 3: This preliminary mapping was moved into file gra_upasarga_map.txt,
      and edited manually.
Note 4: In the second run, this mapping file was used to generate
      gra_preverb0.txt
Sample lines:
;; Case 0006: L=132, k1=aNg, #upasargas=0, upasargas=
;; Case 0007: L=144, k1=ac, #upasargas=2, upasargas=apa,sam
;; Case 0008: L=169, k1=aj, #upasargas=10, upasargas=apa,aBi,ava,A,ud,upa,nis,vi,sam,upA


* gra_preverb1.txt
python preverb1.py slp1 gra_preverb0.txt gra_verb_filter_map.txt mwverbs1.txt gra_preverb1.txt
python preverb1.py deva gra_preverb0.txt gra_verb_filter_map.txt mwverbs1.txt gra_preverb1_deva.txt


The number of upasargas found is reported on a line for the verb entry.
The first GRA verb entry has no upasargas:
;; Case 0001: L=11, k1=aMh, k2=aMh, code=V, #upasargas=0, mw=aMh (same)

The seventh GRA verb entry has 7 upasargas:
```
;; Case 0006: L=132, k1=aNg, k2=aNg, code=V, #upasargas=0, mw=aNg (same)
;; Case 0007: L=144, k1=ac, k2=ac, code=V, #upasargas=2 (1/1), mw=ac (same)
01        apa         ac                 apAc                 apAc yes apa+ac
02        sam         ac                samac                samac no 
```
For each upasarga, an attempt is made to match the prefixed verb to a
known MW prefixed verb.  
In this example, one prefixed forms was found among MW verbs (apAc);
and one  prefixed forms was not found among MW verbs (samac)

Altogether, there are currently 2026 prefixed forms.
Of these, 1791 are matched to MW verbs ('yes' cases), 
and 235 are not matched to MW verbs ('no' cases).


