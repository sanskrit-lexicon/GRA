# literary source markup work based on ../temp_graab_6.txt

extract_ls1_AB.txt and extract_ls1_local_AB.txt from Andhrabharati.
See issue31


---------------------------
../change_7a.txt
3 matches for "</ls>; {" in buffer: temp_graab_6.txt
3 AV changes  (; </
Other misc changes


# install changes
python ../updateByLine.py ../temp_graab_6.txt ../change_7a.txt ../temp_graab_7a.txt
89186 lines read from ../temp_graab_6.txt
89186 records written to ../temp_graab_7a.txt
5 change transactions from ../change_7a.txt
------------------------------------------------------------
# ../change_7b.txt
# deal with problem of non-unique local abbreviations
# add one or more '&#xA0;' (html space) to abbreviations to
# force uniqueness of tooltip for abbreviation.

python ls_local_nonunique.py ../temp_graab_7a.txt ../change_7b.txt

python ../updateByLine.py ../temp_graab_7a.txt ../change_7b.txt ../temp_graab_7b.txt
------------------------------------------------------------
Correction to extract_ls1_AB.txt at line 49
old:
Kir,	Kirātārjunīya, Calcutta ed., 1814	:1
new:
Kir.	:Kirātārjunīya, Calcutta ed., 1814	:1

------------------------------------------------------------
extract_ls_local.txt

python extract_ls_local.py ../temp_graab_7b.txt extract_ls_local.txt
Bollensen	:Zur Herstellung des Veda.— Bollensenʼs Article in Orient und Occident	:7
 l
------------------------------------------------------------
../change_7c.txt   2 changes
extract_ls1a_AB.txt  4 lines commented out.

# check local and global ls abbreviations

python check_ls_global_local.py ../temp_graab_7b.txt extract_ls_local.txt extract_ls1_AB.txt

WARNING: local+global: dup=Be. vollst. Gramm.
prev tip: (1) Vollständige Grammatik der Sanskrit Sprache— Benfey, 1852
cur  tip: (1) Vollständige Grammatik der Sanskrit Sprache— Benfey, 1852
solution: change_7c:  remove ab="..."
------
WARNING: local+global: dup=Goldschmidt in Beitr.
prev tip: (1) Etymologien. 1. chromŭ - srāma; 2. juvā́ku— Goldschmidtʼs Article in Beiträge zur vergleichenden Sprachforschung
cur  tip: (1) ?? Goldschmidtʼs Article in Beiträge
solution: comment out global tip in extract_ls1a_AB.txt
-------
WARNING: local+global: dup=Goldschmidt in Beiträge
prev tip: (1) Etymologien. 1. chromŭ - srāma; 2. juvā́ku— Goldschmidtʼs Article in Beiträge zur vergleichenden Sprachforschung
cur  tip: (1) ?? Goldschmidtʼs Article in Beiträge
solution: comment out global tip in extract_ls1a_AB.txt
-------

WARNING: local+global: dup=Lottner
prev tip: (1) Ueber die stellung der Italer innerhalb des indoeuropäischen stammes (schlufs)— Lottnerʼs Article in Kuhnʼs Zeitschrift
cur  tip: (1) Lottner
solution: comment out global tip in extract_ls1_AB.txt
-------

WARNING: local+global: dup=Max Müller
prev tip: (1) Oxford Essays— Max Müller, 1856
cur  tip: (2) Max Müllerʼs edition of Rig-Veda
solution: comment out global tip in extract_ls1_AB.txt
------
5 abbrev dups local+global

# install 7c changes
python ../updateByLine.py ../temp_graab_7b.txt ../change_7c.txt ../temp_graab_7c.txt
1 change transactions from ../change_7c.txt
1 of type new

------
extract_ls1_local.txt

python extract_ls_local.py ../temp_graab_7c.txt extract_ls1_local.txt
38 lines written to extract_ls1_local.txt 
------------------------------------------------------------
# try the check of dups AGAIN with revised inputs
python check_ls_global_local.py ../temp_graab_7c.txt extract_ls1_local.txt extract_ls1a_AB.txt

38 TipRead records from extract_ls1_local.txt
97 TipRead records from extract_ls1a_AB.txt
0 abbrev dups local
0 abbrev dups global
0 abbrev dups local+global
False  compare set1 and set2
set1 - set2 =  {'Bollens.', 'F.', 'Boll.', 'Bollensen', 'Ku. in Zeitschr.', 'C.', "BR.'s Vermuthung", 'Iliad, Homer'}
set2 - set1 =  set()


'Bollens.' etc appear as <ls>X</ls> in temp_graab_7c.txt, but are not
 present in extract_ls1a_AB.txt.

extract_ls1b_AB.txt
Solution:  Add records to ls1b
Bollensen       :?      :6
F.      :?      :1
Bollens.        :?      :2
Ku. in Zeitschr.        :?      :2
C.      :?      :2
Boll.   :?      :1
BR.'s Vermuthung        :?      :2
Iliad, Homer    :?      :1

TODO: Andhrabharati to resolve these

-----------------------------------------------------------

python check_ls_global_local.py ../temp_graab_7c.txt extract_ls1_local.txt extract_ls1b_AB.txt

WARNING: local+global: dup=Bollensen
prev tip: (1) Zur Herstellung des Veda.— Bollensenʼs Article in Orient und Occident
cur  tip: (6) ?

solution: change local abbreviation to 'Bollensen&#xA0;'
add this change to change_7d.txt

# install temp_graab_7d.txt
python ../updateByLine.py ../temp_graab_7c.txt ../change_7d.txt ../temp_graab_7d.txt
1 change transactions from ../change_7d.txt
------------------------------------------------------------
; extract_ls2_local.txt
python extract_ls_local.py ../temp_graab_7d.txt extract_ls2_local.txt

python check_ls_global_local.py ../temp_graab_7d.txt extract_ls2_local.txt extract_ls1b_AB.txt

38 TipRead records from extract_ls2_local.txt
105 TipRead records from extract_ls1b_AB.txt
0 abbrev dups local
0 abbrev dups global
0 abbrev dups local+global
True  compare set1 and set2
set1 - set2 =  set()
set2 - set1 =  set()

FINALLY!

------------------------------------------------------------
# install revised graauth/tooltip.txt in csl-pywork
cat extract_ls1b_AB.txt extract_ls2_local.txt > extract_ls_all.txt

# change format to that of tooltip.txt in csl-pywork
python make_graauth_tooltip_2.py extract_ls_all.txt temp_tooltip.txt

142 abbreviations read from extract_ls_all.txt
142 lines written to temp_tooltip.txt

$ wc -l extract_ls_all.txt
147 extract_ls_all.txt

$ grep -E '^;' extract_ls_all.txt
; Lottner       :Lottner        :1
;Max Müller     :Max Müllerʼs edition of Rig-Veda       :2

cp temp_tooltip.txt /c/xampp/htdocs/cologne/csl-pywork/v02/distinctfiles/gra/pywork/graauth/tooltip.txt
-------------------------------------------------------
06-24-2023
revise extract_ls1b_AB.txt per
 https://github.com/sanskrit-lexicon/GRA/issues/31#issuecomment-1605253081
 https://github.com/sanskrit-lexicon/GRA/issues/31#issuecomment-1605266000
sh redo_tooltip.sh

142 abbreviations read from extract_ls_all.txt
142 lines written to temp_tooltip.txt
145 extract_ls_all.txt
; Co. Text      :Codice Text [Rigveda Saṃhitā Text, Chambersʼ Manuscript No. ?? :1
; Lottner       :Lottner        :1
;Max Müller     :Max Müllerʼs edition of Rig-Veda       :2

-------------------------------------------------------
 temp_graab_7.AB.txt
   (Ref: https://github.com/sanskrit-lexicon/GRA/issues/31#issuecomment-1605276250)
diff ../temp_graab_7d.txt ../temp_graab_7.AB.txt > tempdiff7d_AB.txt
wc -l  tempdiff7d_AB.txt
-------------------------------------------------------
../change_7e.txt
Miscellaneous changes based on temp_graab_7.AB.txt

python extract_ls_local.py ../temp_graab_7.AB.txt temp_ls_local_AB7.txt
Bollensen	:Zur Herstellung des Veda.— Bollensenʼs Article in Orient und Occident	:7

python make_change_bollensen.py ../temp_graab_7d.txt temp_change_bollensen.txt
# insert temp_change_bollensen.txt changes into changes_7e.
14 changes written to temp_change_bollensen.txt

python ../updateByLine.py ../temp_graab_7d.txt ../change_7e.txt ../temp_graab_7e.txt
17 change transactions from ../change_7e.txt

diff ../temp_graab_7e.txt ../temp_graab_7.AB.txt > diff7e_AB.txt
wc -l  diff7e_AB.txt
8 diff7e_AB.txt

Two remaining differences
line 71433
  7 (cdsl) Ku. in Zeitschr.&#xA0;
  7.AB. Ku. in Zeitschr.
line 58890.
  7 (cdsl) <ls n="AV.">11,2,24</ls>  per AB's suggestion!
  8.AB. <ls n="AV.">11,1,2</ls>.
--------------------------------------------------------
Reexamine the local and global abbreviations

------------------------------------------------------------
; extract_ls3_local.txt
python extract_ls_local.py ../temp_graab_7e.txt extract_ls3_local.txt
42 lines written to extract_ls3_local.txt

------------------------------------------------------------
; extract_ls1c_AB.txt
cp extract_ls1b_AB.txt extract_ls1c_AB.txt

Revise extract_ls1c_AB.txt
 -- removals
   Bollens.	:?	:2
   Boll.	:?	:1
   Ku. in Zeitschr.	:?	:2
   ; Co. Text	:Codice Text [Rigveda Saṃhitā Text, Chambersʼ Manuscript No. ??	:1
   ; Lottner	:Lottner	:1
   ;Max Müller	:Max Müllerʼs edition of Rig-Veda	:2

 -- changes
 1) old: Iliad, Homer	:?	:1
    new: Iliad— Homer	:Iliad of Homer	:1
 2) old: Text	:Rigveda Saṃhitā Text	:48
    new: Text	:Rigveda Saṃhitā Text	:49
 
python check_ls_global_local.py ../temp_graab_7e.txt extract_ls3_local.txt extract_ls1c_AB.txt
42 TipRead records from extract_ls3_local.txt
99 TipRead records from extract_ls1c_AB.txt

------------------------------------------------------------
# install revised graauth/tooltip.txt in csl-pywork
cat extract_ls1c_AB.txt extract_ls3_local.txt > extract_ls_all.txt

# change format to that of tooltip.txt in csl-pywork
python make_graauth_tooltip_2.py extract_ls_all.txt temp_tooltip.txt

142 abbreviations read from extract_ls_all.txt
142 lines written to temp_tooltip.txt

$ wc -l extract_ls_all.txt
147 extract_ls_all.txt

$ grep -E '^;' extract_ls_all.txt
; Lottner       :Lottner        :1
;Max Müller     :Max Müllerʼs edition of Rig-Veda       :2

cp temp_tooltip.txt /c/xampp/htdocs/cologne/csl-pywork/v02/distinctfiles/gra/pywork/graauth/tooltip.txt
------------------------------------------------------------
06-25-2023  
; extract_ls1d_AB.txt
cp extract_ls1c_AB.txt extract_ls1d_AB.txt

Revise extract_ls1d_AB.txt
 Ref: https://github.com/sanskrit-lexicon/GRA/issues/31#issuecomment-1605879922
 
Chamb. 60 :Chambers 60 [Rigveda Padapāṭha Aṣṭakas 1-4, Chambersʼ Manuscripts collection No. 60] :2
Naigh. :Naighaṇṭukakāṇḍa [Jâskaʼs Nirukta, sammt den Nighaṇṭavas Bd. 1— Rudolf Roth, 1852] :21
Nir. :Nirukta [Jâskaʼs Nirukta, sammt den Nighaṇṭavas Bd. 2— Rudolf Roth, 1852] :12
P. :Rig-Veda Padapāṭha :25
Pad. :Rig-Veda Padapāṭha :167
Pada :Rig-Veda Padapāṭha :73
Pada bei Aufr. :Rig-Veda Padapāṭha, Aufrechtʼs edition :1
Padap. :Rig-Veda Padapāṭha :7
Padapāṭha :Rig-Veda Padapāṭha :2
 
python check_ls_global_local.py ../temp_graab_7e.txt extract_ls3_local.txt extract_ls1d_AB.txt
42 TipRead records from extract_ls3_local.txt
99 TipRead records from extract_ls1d_AB.txt

------------------------------------------------------------
# install revised graauth/tooltip.txt in csl-pywork
cat extract_ls1d_AB.txt extract_ls3_local.txt > extract_ls_all.txt

# change format to that of tooltip.txt in csl-pywork
python make_graauth_tooltip_2.py extract_ls_all.txt temp_tooltip.txt

141 abbreviations read from extract_ls_all.txt
141 lines written to temp_tooltip.txt

$ wc -l extract_ls_all.txt
141 extract_ls_all.txt

$ grep -E '^;' extract_ls_all.txt
 (NONE): No comment lines present.

cp temp_tooltip.txt /c/xampp/htdocs/cologne/csl-pywork/v02/distinctfiles/gra/pywork/graauth/tooltip.txt

------------------------------------------------------------
