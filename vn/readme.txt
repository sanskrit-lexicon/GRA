Conversion of corrections to metaline format.
 Must be coordinated with gra.txt

current directory in local machine
cd /c/xampp/htdocs/sanskrit-lexicon/gra/vn/orig

-----------------------------------------------------------
temp_gra_0.txt
  from csl-orig at commit 29055d35d8b5b6a42959b0487cb09d2e294f76a0
cd /c/xampp/htdocs/cologne/csl-orig/v02/gra/
git show 29055d35d:/v02/gra/gra.txt > temp_gra_29055d35d.txt
# move to this directory
cd /c/xampp/htdocs/sanskrit-lexicon/gra/vn
mv /c/xampp/htdocs/cologne/csl-orig/v02/gra/temp_gra_29055d35d.txt temp_gra_0.txt

-----------------------------------------------------------
vn files
Start with orig/grassmann_Nachtraege_utf8.txt

-----------------------------------------------------------
orig/vn0.txt  page breaks
Manually edited from grassmann_Nachtraege_utf8/txt
* put an initial page at top of file ([page1741])
* have page breaks on separate lines

-----------------------------------------------------------
orig/vn1.txt  headwords
vn0.txt does not provide headwords!  
Rather, corrections are indicated by page,line
pages 1741-1748.

Then, there are Nachträge (supplements)
pages 1749-1774.
Format <p><b>X:</b>  X is headword (in iast)
or <p>h. <b>X:</b>   (h is homonym)
<p>2. <b>sahá:</b>
last one is <p><b>sthávira:</b>


page 1748 after
<h>Zu streichen (* bedeutet, dass das Ganze zu streichen ist):</h>
   To be deleted (* means that the whole thing is to be deleted)
first: <p>3,28. a: 63,7
last : <p>1608,4.3.b v. u.: (der Blitz)
Line count may be from bottom of page ('b.')
  <p>20,16. b v. u.: -āṇi st. -āni

364 matches for "^<p>[0-9]+,[0-9]+" in buffer: vn0.txt
Add numbering to the corrections 
  Example:
  OLD: <p>3,28. a: 63,7
  NEW: <c 1>1 <p>3,28. a: 63,7
  
python correction_num.py orig/vn0.txt orig/vn1.txt
2922 read from orig/vn0.txt
364 lines labeled
2922 written to orig/vn1.txt

Several manual editing changes to vn1:
<h>ENGLISH... several places. These for my information.

deletions:
 Zu streichen (* bedeutet, dass das Ganze zu streichen ist)
 <c 273> through <c 364>
 Similar format currently. But change <c N> to <d N>

change to <d 273>,etc
  These are identified as 

----------------------------------------------------------------
vn2
 Label the additions <a N>
  lines start with '<p><b>' or '<p>*<b>'
python addition_num.py orig/vn1.txt orig/vn2.txt
2928 read from orig/vn1.txt
636 lines labeled
2928 written to orig/vn2.txt
----------------------------------------------------------------

Need to change (in vn2)
1. ṙ -> ṛ  166 changes
----------------------------------------------------------------
vn3 is same as vn2, but with some further changes
1. Transcoding changes -- aim for consistency with gra.txt conventions
     which in turn aims to be consistent with IAST conventions.
     See Author's note below regarding his 'iast' conventions.
     e10 (e-roof) -> aí (slp1 E/) 16 changes
     e1  (e-macron) -> ai  (slp1 E) 21 changes
     o10 (o-roof) -> aú  (slp1 O/) 9
     o1  (o-macron) -> au (slp1 O) 16
     y4a (y-acute+a) -> yà (svarita accent)  4
     y4u (y-acute+u) -> yù (svarita accent)  1
     â (a-roof)  -> ā́  (slp1 A/)  525
     î (i-roof)  -> ī́  (slp1 I/) 80
     û (u-roof) -> ū́  (slp1 U/)  0 (none of these)
     ū0 -> ū́ (slp1 U/) 47
     ṅs -> ṃs   (slp1 Ns -> Ms) 20
     ṅś -> ṃś   (slp1 NS -> MS)  4
     ṅṣ -> ṃṣ   (slp1 Nz -> Mz)  2
     ṅh -> ṃh   (slp1 Nh -> Mh)  5
     
--------------------------------------------------
From Front matter English translation
Ref: https://sanskrit-lexicon.uni-koeln.de/scans/csldev/csldoc/build/dictionaries/prefaces/grapref/grapref06.html

I do diverge from Aufrecht’s transcription where he represents a single sound
by two letters, as these relations can be highly confusing in a dictionary.
For this end, I write
ṙ instead of ṛi, r̄ instead of ṙî, ṣ instead of sh, ē instead of ai, and
ō instead of au.
These last two spellings cannot give rise to confusion. For comparative works,
these two as well as the characters e and o have to be avoided and
e=ai, o=au, ē=āi, ō=āu should be used.
The composite spelling has been preserved for aspirated stops.
This is admissible because they are placed in the same position in the
lexicographic order, regardless of whether they are treated as a single
or two letters.
I also preserved the compound sign ḷi, as it only occurs in the root kalp.

In the representation of the accents, I deviate (from Aufrecht),
in that I indicate
the accent-less long vowel by a macron and
the accented long vowel by a roof (^) –
so ā instead of â, â instead of ấ –
and in that I represent svarita by an accent on the preceding semi-vowel (y, v),
e.g. asmadrýac instead of asmadryàc.
--------------------------------------------------------------
2. <p>118 Ueberschrift: arvācīná st. avācīná
   wrong form in vn. Any change to make?
-------------------------------------------------------------
-------------------------------------------------------------
Scan page error (corrected)
https://github.com/sanskrit-lexicon-scans/gra/blob/main/pdfpages/pg_1769.pdf
Shows pages 1761,2  (should be pages 1769,70)
  
  
Note: This page correctly available at vn/gra_bayer_nachtraege_pp1741-1776.pdf
Correct pg_1769.pdf installed at cologne, sanskrit-lexicon-scans/gra/
and local cologne/scans/gra/


-------------------------------------------------------------
python diff_to_changes_dict.py orig/temp_gra_0.txt orig/temp_gra_1.txt orig/change_gra_1.txt
264 changes written to change_gra_1.txt
-------------------------------------------------------------
