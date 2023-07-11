gra/graab/meta2/readme.txt
Begin 06-30-2023

----------------------------------------------------------------------
check_ea1.txt
python check_ea1.py ../temp_graab_9.txt check_ea1.txt
163 extended ascii codes found in ../temp_graab_9.txt

correction to remove two instances of "(\u200e)     2 := LEFT-TO-RIGHT MARK"
../change_9c.txt
python ../updateByline.py ../temp_graab_9b.txt ../change_9c.txt ../temp_graab_9c.txt
2 change transactions from ../change_9c.txt

cp ../temp_graab_9c.txt ../temp_graab_9.txt

Recalc check_ea1
python check_ea1.py ../temp_graab_9.txt check_ea1.txt
162 extended ascii codes found in ../temp_graab_9.txt

----------------------------------------------------------------------
RV citation corrections.
Ref: https://github.com/sanskrit-lexicon/GRA/issues/32#issuecomment-1615568613
Ref: https://github.com/sanskrit-lexicon/GRA/issues/32#issuecomment-1615596159
Changes added to ../change_9c.txt
python ../updateByline.py ../temp_graab_9b.txt ../change_9c.txt ../temp_graab_9c.txt
11 change transactions from ../change_9c.txt

cp ../temp_graab_9c.txt ../temp_graab_9.txt
python /c/xampp/htdocs/cologne/xmlvalidate.py dev9/pywork/gra.xml dev9/pywork/gra.dtd

1. under gur, <ls>dhātupāṭha</ls>
 - new ls abbrev (only instance)
 Refer litsrc1/readme.txt
 
2. under siv, <ab>Verg. Aen.</ab> -> <ls>Verg. Aen.</ls>

 - remove normal abbreviation <ab>Verg. Aen.</ab> (this is only instance)
    old: Verg. Aen.	<id>Verg. Aen.</id> <disp>Vergleiche Aenderung</disp>
   See abbrevs1/readme.txt
   
 - add new ls abbrev:  <ls>Verg. Aen.</ls>
   See litsrc1/readme.txt   ls1f
---------------------------------------------------------------
07-03-2023
860 matches in 797 lines for "</ls> 〔" in buffer: temp_graab_9.txt
"<ls>X></ls> 〔N〕"  -> "<ls>X> 〔N〕</ls>"
../change_9d.txt

python make_change_9d.py ../temp_graab_9c.txt temp_change_9d.txt
807 lines changed

cp temp_change_9d.txt ../change_9d.txt
# manual editing of ../change_9d.txt

python ../updateByline.py ../temp_graab_9c.txt ../change_9d.txt ../temp_graab_9d.txt
# 834 change transactions from ../change_9d.txt

cp ../temp_graab_9d.txt ../temp_graab_9.txt
-------------------------------------------------------------
../change_9e.txt
Remove 🞄 (\u1f784) 106 := BLACK SLIGHTLY SMALL CIRCLE
Ref: https://github.com/sanskrit-lexicon/GRA/issues/32#issuecomment-1615747576
../temp_graab_9e.txt

python ../updateByline.py ../temp_graab_9d.txt ../change_9e.txt ../temp_graab_9e.txt
6 lines changed

cp ../temp_graab_9e.txt ../temp_graab_9.txt
-----------------------------------------------------------
../change_9f.txt
----------
PART ONE
Ref: https://github.com/sanskrit-lexicon/GRA/issues/32#issuecomment-1616331226

<ab n="Vorige">V.</ab> → <ab n="Vers">V.</ab>


----------
PART TWO
Ref: https://github.com/sanskrit-lexicon/GRA/issues/32#issuecomment-1615898475
replace n̆̇ with n̐; and update counts accordingly--
;; delete ̆ (\u0306) 0 := COMBINING BREVE
;; delete ̇ (\u0307) 0 := COMBINING DOT ABOVE
;; update ̐ (\u0310) 7 := COMBINING CANDRABINDU

Add to list of combining characters:
  r'\u0310', # combining candrabindu
  r'\u0323', # combining dot below
  r'\u05bc', # HEBREW POINT DAGESH OR MAPIQ
  r'\u05b0', # HEBREW POINT SHEVA
  r'\u05b5', # HEBREW POINT TSERE

----------
PART THREE
apostrophe -> ʼ (\u02bc)   MODIFIER LETTER APOSTROPHE
ref: https://github.com/sanskrit-lexicon/GRA/issues/32#issuecomment-1619184150
176 changes in 149 lines

---------
PART FOUR
; PART FOUR
; Ref: https://github.com/sanskrit-lexicon/GRA/issues/32#issuecomment-1616730883
; <gk>στῆ δ ̓ ὀρϑός</gk> as <gk>στῆ δ᾽ ὀρϑός</gk>

---------
PART FIVE
; restore normal apostrophes:  ' = IAST avagraha
; 4 changes
---------
PART SIX
; restore normal apostrophes (German)
; 2 changes
 
--------
python ../updateByline.py ../temp_graab_9e.txt ../change_9f.txt ../temp_graab_9f.txt
195 lines changed
cp ../temp_graab_9f.txt ../temp_graab_9.txt

cd ../
sh redo.sh
python /c/xampp/htdocs/cologne/xmlvalidate.py dev9/pywork/gra.xml dev9/pywork/gra.dtd
-----------------------------------------------------
python check_ea2.py ../temp_graab_9.txt check_ea2.txt
89186 lines in ../temp_graab_9.txt
155 extended ascii codes found in ../temp_graab_9.txt
54 LATIN
78 GREEK
 3 HEBREW
20 the rest
-----------------------------------------------------------
Compare the extended ascii counts in temp_graab_9 and temp_graab_9_AB:
diff check_ea2.txt temp_check_ea2_graab_9_AB.txt
44a45
> ̓  (\u0313)     1 := COMBINING COMMA ABOVE
132d132
< ᾽  (\u1fbd)     1 := GREEK KORONIS
147a148
> ⁾  (\u207e)     2 := SUPERSCRIPT RIGHT PARENTHESIS
153,154c154,155
< 〔  (\u3014)   896 := LEFT TORTOISE SHELL BRACKET
< 〕  (\u3015)   896 := RIGHT TORTOISE SHELL BRACKET
---
> 〔  (\u3014)   895 := LEFT TORTOISE SHELL BRACKET
> 〕  (\u3015)   895 := RIGHT TORTOISE SHELL BRACKET
155a157
> 🞄  (\u1f784)   106 := BLACK SLIGHTLY SMALL CIRCLE

Only problem is with the tortoises!

-----------
What is the difference?

python check_tortoise.py ../temp_graab_9.txt temp_check_tortoise.txt
896 instances found
807 records written to temp_check_tortoise.txt

python check_tortoise.py ../temp_graab_9_AB.txt temp_check_tortoise_AB.txt
895 instances found
807 records written to temp_check_tortoise_AB.txt

 diff temp_check_tortoise.txt temp_check_tortoise_AB.txt
699c699
< 74407 〔578〕 : 〔10,315〕
---
> 74407 〔578〕

AB: <ab>Verg. Aen.</ab> {10,315};
CDSL: <ls>Verg. Aen. 〔10,315〕</ls>

In this case, CDSL is accepted.
-----------------------------------------------------------
../change_9g.txt
 change <ls ab="X">Y</ls> to <ls>Y</ls>
63 changes in 60 lines

Note:
12 matches in 9 lines for "<ls[^>]" in buffer: temp_graab_9g.txt
 These are all AV. links, e.g. <ls n="AV.">14,1,57</ls>.
----

python ../updateByline.py ../temp_graab_9f.txt ../change_9g.txt ../temp_graab_9g.txt

cp ../temp_graab_9g.txt ../temp_graab_9.txt

cd ../
Change one.dtd: (csl-pywork/v02/makotemplates/pywork/)
Remove <!-- <!ATTLIST ls ab CDATA #IMPLIED> GRA -->

sh redo.sh
python /c/xampp/htdocs/cologne/xmlvalidate.py dev9/pywork/gra.xml dev9/pywork/gra.dtd
  ok
  
-----------------------------------------------------------
07-11-2023
gra-meta2_1.txt  REVISION OF gra-meta2-0.txt.
------
-----------------------------------------------------------
