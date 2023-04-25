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
python diff_to_changes_dict.py temp_gra_0.txt temp_gra_1.txt change_gra_1.txt
264 changes written to change_gra_1.txt
-------------------------------------------------------------
vn3_1_AB.txt
  Andhrabharati corrections to vn3 - the 'corrections' <c n> items.
  I changed tab character to ' ::AB:: ' which is more readable to me.
----
vn3_1.txt
  cp vn3.txt vn3_1.txt
  Manual changes per vn3.1_AB.txt
 changes:
1.  add '-a' and '-b' to some page breaks
  Principle: the 3-column 'print' pages have two page numbers N1 and N2
    first two column breaks marked as [PageN1-a] and [PageN1-b].
    3rd column break marked as [PageN2].
2. Misc. corrections from AB (marked as ';; x')
    210:<c 100> <p>393,21.a v. u.: -ánti  ::AB:: st. anti ;;could this be -anti ?
    Jim: yes Should be '-anti'.
    305:<c 147> <p>742,15: bŕhaspátim  ::AB:: st. agním ;; print error <p>342 instead of <p>742!!
   (JIM)    NO:  page 742,15 is correct. agním is to be corrected to bŕhaspátim
            
    350:<c 169> <p>991,15.b: -āmahe  ::AB:: st. -āmahaí ;;(e-roof) -> aí
      Also change temp_gra_1.txt
    556:<c 270> <p>1513,17 v. u.: -ásya  ::AB:: st. -asya ;;print error <p>5113 instead of <p>1513!!
    600:<d 287> <p>149,20.21.a: pári bis 61,8 ;;print error 20,21 instead of 20.21
    711:<p>1051,9.10: * ;;print error 1051.9 instead of 1051,9
      Digitization error. This is a deletion (of all of lines 9,10
      <d 342> <p>1051.9.10: *
     Also, renumbered the remaining <d N> in VN
       <d 342> -> <d 343>
       <d 343> -> <d 344>
       ...
       <d 364> -> <d 365>
     
3. change 'a :' to 'a:'
   10 matches for " a:" in buffer: vn3_1.txt
    230:<c 110> <p>473,25. a: 459 st. 659
    342:<c 165> <p>966,10. a: 734,2 st. 724,2
    344:<c 166> <p>972,29. a: 849,2. 3 st. 849,23
    402:<c 195> <p>1118,12. a: 776,19 st. 976,19
    572:<d 273> <p>3,28. a: 63,7
    600:<d 287> <p>149,20.21. a: pári bis 61,8
    602:<d 288> <p>150,8. 9. a: suvī́ras 491,9
    610:<d 292> <p>163,5. a: 844,14
    660:<d 317> <p>382,14. a: 1) 130,9
    664:<d 319> <p>448,30. a: 376,4.
4. change 'b :' to 'b:'
   6 matches for " b:" in buffer: vn3_1.txt
      8:<c 1> <p>2,4. b: 204,1 statt 204,2
    178:<c 84> <p>337,22. b: 2 st. 3
    238:<c 114> <p>488,4. b: -yúṣas st. -úṣas
    362:<c 175> <p>1008,31. b: 612,2 st. 612,3
    616:<d 295> <p>186,11. b: [A. p.]
    676:<d 325> <p>528,29. 30. b: *
5. remove space before line-number
    119:<c 55> <p>168,4. 5: <i>Schlangenstösser</i> (Raubvogel) st. <i>wie ... schiessend</i>
    602:<d 288> <p>150,8. 9.a: suvī́ras 491,9
    676:<d 325> <p>528,29. 30.b: *
    745:<d 359> <p>1446,31. 30.b v. u.: nā́kam bis 50
---------    
Corrections to make in vn3.1_AB.txt

1. line 54
OLD: <c 24> <p>52,3 v. u.: 638,2 st. 638,1
NEW: <c 24> <p>52,3.b v. u.: 638,2 st. 638,1

2. line 82
OLD: <c 38> <p>100,4.b: 780,9 st. 780
NEW: <c 38> <p>100,3.b: 780,9 st. 780

3. line 88
OLD: <c 40> <p>132,22.b: -ā́ṇi st. -ā́ni
NEW: <c 40> <p>132,21.b: -ā́ṇi st. -ā́ni

4. line 115
OLD: <c 53> <p>159,21.22: <i>nicht gleitend</i> st. <i>nicht ... zuckend.</i>
NEW: <c 53> <p>159,21.22: <i>nicht gleitend</i> st. <i>nicht zuckend</i>

5. line 131
OLD: <c 61> <p>211,7.b: 1.7; st. 1,7;
NEW: <c 61> <p>211,7.b: 1. 7; st. 1,7;

6. line 135
OLD: <c 63> <p>213,28.b v. u.: 106,1.6. st. 106,1.5.
NEW: <c 63> <p>213,28.b v. u.: 106,1. 6. st. 106,1.5.

7. line 140
OLD: <c 65> <p>216,20.21.a: 658,1--9 st. 658,1.9
NEW: <c 65> <p>216,20.21.a: 658,1--9 st. 658,1. 9

8. line 299
OLD: <c 144> <p>730,9.b: vayám st. vāyávas
NEW: <c 144> <p>729,9.b: vayám st. vāyávas

9. line 479
OLD: <c 233> <p>1348,6.a: 640,12 st. 640,11
NEW: <c 233> <p>1348,6.b: 640,12 st. 640,11   [vn print error]

------------------------------------------
¥  also under <a 282> gah
   vn3_1.txt changes all 55 ¥ to 〰  (u+3030 WAVY DASH)
------------------------------------------
   
£ change to ‿ (\u203f) UNDERTIE  (11 changes)
  joins two vowels (hiatus?). Used in cdsl gra.txt (ref gra-meta2.txt)
  
------------------------------------------
n1 change to ṅ (7 changes)
------------------------------------------
... -> …  (2) in vn3_1.txt

------------------------------------------
temp_gra_2.txt
cp temp_gra_1.txt temp_gra_2.txt
manual changes:
5897 matches in 4478 lines for "…" in buffer: temp_gra_2.txt
  change these to 〰  (u+3030 WAVY DASH)
python diff_to_changes_dict.py temp_gra_1.txt temp_gra_2.txt change_gra_2.txt
4478 changes written to change_gra_2.txt
------------------------------------------
temp_gra_3.txt
cp temp_gra_2.txt temp_gra_3.txt
manual changes:

278 matches in 266 lines for "\.\.\." in buffer: temp_gra_1.txt
  change these to ellipsis …

python diff_to_changes_dict.py temp_gra_2.txt temp_gra_3.txt change_gra_3.txt

NOTE: See below for comment about other possible errors
with period and ellipsis

----------------------------------------------------------------------------
vn3_1 RDQM  -> LDQM  ” -> “  (5)
5 matches for "”" in buffer: vn3_1.txt  RDQM
” = U+201D = RIGHT DOUBLE QUOTATION MARK

“ = U+201C = LEFT DOUBLE QUOTATION MARK
„ = u+201E = DOUBLE LOW-9 QUOTATION MARK
   In some fonts, U+201D and U+201C look the same
German quotations: (201E)text(201C)

Ref: https://en.wikipedia.org/wiki/Quotation_mark
   The German tradition preferred the curved quotation marks,
    the first one at the level of the commas,
    the second one at the level of the apostrophes:
    „…“.
    Alternatively, these marks could be angular and in-line with
    lower case letters, but still pointing inward: »…«.

------------------------------------------
temp_gra_4.txt
cp temp_gra_3.txt temp_gra_4.txt

59 matches in 31 lines for "“" in buffer: temp_gra_4.txt   U201C LEFT DOUBLE QUOTATION MARK
982 matches in 588 lines for "”" in buffer: temp_gra_4.txt U201D RIGHT DQM

manual changes to temp_gra_4.txt

1.
LDQM  -> DLQM  “ -> „  (59)  
2.
RDQM -> LDQM ” -> “ (982)

python diff_to_changes_dict.py temp_gra_3.txt temp_gra_4.txt change_gra_4.txt
588 changes written to change_gra_4.txt

Totals after these changes:
  ” U+201D  0
  “ U+201C 982 LDQM
  „ U+201E 991 DLQM

----------------------------------------------------------------------------
temp_gra_5.txt
cp temp_gra_4.txt temp_gra_5.txt

THERE ARE SOME MISMATCHES (991 != 982)

python quote_counts.py temp_gra_4.txt temp_quote_counts_1.txt
22 lines with mismatched „  “

# manual corrections of temp_gra_5 using temp_quote_counts_1.txt
# generate change file.
python diff_to_changes_dict.py temp_gra_4.txt temp_gra_5.txt change_gra_5.txt
38 changes written to change_gra_5.txt

# check quote counts again with change_gra_5
python quote_counts.py temp_gra_5.txt temp_quote_counts_2.txt
0 quote character mismatches
0 written to temp_quote_counts_2.txt

Totals after these changes:
  ” U+201D  0
  “ U+201C 986 LDQM
  „ U+201E 986 DLQM

---------------------------------------------------------------------------------------
    
---------------------------------------------------------------------------------------
temp_gra_6.txt
cp temp_gra_5.txt temp_gra_6.txt

304 lines in temp_gra_5.txt starting with one period.
304 matches in 200 lines for "^\.[^.]" in buffer: temp_gra_5.txt

# Apply manual changes to temp_gra_6.txt
# Generate change_6
python diff_to_changes_dict.py temp_gra_5.txt temp_gra_6.txt change_gra_6.txt
521 changes written to change_gra_6.txt

---------------------------------------------------------------------------------------
Observation:
188 matches in 170 lines for "\.\." in buffer: temp_gra_6.txt
7 matches for "\. +\." in buffer: temp_gra_6.txt

Not sure of significance of
'..'
'. .'
〰
…  (in print, ...)


------------------------------------------


-----------------------------------------------------------------
# CANNOT DO THIS PROPERLY! (since there is temporary markup like <c 5>X</c> which is
not well-formed xml.

#  temp_gra_1.txt has some 'temporary' markup such as <c 7>X</c>
# install temp_gra_1.txt into csl-orig
# assume in vn directory
cp orig/temp_gra_1.txt /c/xampp/htdocs/cologne/csl-orig/v02/gra/gra.txt
cd /c/xampp/htdocs/cologne/csl-pywork/v02
grep gra redo_xampp_all.sh
sh generate_dict.sh gra  ../../gra

====================================================================
AT THIS POINT, THE TWO RELEVANT FILES ARE
vn3_1.txt
temp_gra_6.txt

====================================================================
vn3.1_AB.updated.txt
Various undocumented changes by AB to vn3.1_AB.txt
Analysis of the differences
See orig/vn3ABwork/readme.txt.
A few minor changes by me.
Final version from AB: vn3.1_AB.update_ejf_1.txt
 compare to CDSL version: vn3_1_cd_update.txt
 diffexamine2_update.txt shows the comparison.
  The 50 remaining AB changes are 'good' changes

Conclusion: Use vn3.1_AB.update_ejf_1.txt
# Use renamed copy vn3_2.txt (shorter name)
 cp orig/vn3ABwork/vn3.1_AB.update_ejf_1.txt orig/vn3_2.txt

====================================================================
