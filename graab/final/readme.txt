
../temp_graab_9g_AB.txt
Ref: https://github.com/sanskrit-lexicon/GRA/files/11955037/../temp_graab_9g.AB.zip

diff ../temp_graab_9g.txt ../temp_graab_9g_AB.txt  | wc -l
383

wc -l ../temp_graab*
   89186 ../temp_graab_9g.txt
   89074 ../temp_graab_9g_AB.txt


cp ../temp_graab_9g.txt ../temp_graab_9h.txt
Minor editing  some lines so that the number of lines is same as 9g_AB

diff ../temp_graab_9g.txt ../temp_graab_9h.txt  > diff_9gh.txt

wc -l ../temp_graab*
   89186 ../temp_graab_9g.txt
   89074 ../temp_graab_9g_AB.txt
   89074 ../temp_graab_9h.txt

------------------------------------------------
../change_9h_9gAB.txt
66 lines changed between 9h and 9g_AB
the changes are commented on in ../change_9h_9gAB.txt
Here are a few:
----------
; <L>1090<pc>0119<k1>arz<k2>1. arz, fz
; old: <ls>VS. 〔23,55. 56〕</ls>
; new: <ls>VS. 〔23,55〕</ls>. <ls n="VS. 〔23,">56〕</ls>
---------
; <L>2176<pc>0281<k1>fRa<k2>fRa/
; old: <ls>J. Grimm</ls> [<ls>Ku. 〔1,82〕</ls>]
; new: <ls>J. Grimm [Ku. 〔1,82〕]</ls> 
---------
?
; <L>3517<pc>0490<k1>jihvA<k2>jihvA/
; old: <ls>Lottner</ls> [<ls>Ku. Zeitschr. 〔7,186〕</ls>]
; new: <ls>Lottner [Ku. Zeitschr. 〔7,186〕]</ls>
---------
?
; <L>5643<pc>0834<k1>purUravas<k2>purU-ra/vas
; old: <ls>Max Müller</ls> (<ls>Oxford Essays 〔S. 61〕</ls>)
; new: <ls>Max Müller (Oxford Essays 〔S. 61〕)</ls>
---------
?
; <L>9669<pc>1515<k1>siMha<k2>siMha/
; old: <ls>Aufr. in Ku. Zeitschr.&#xA0; 〔1,356〕</ls>
; new: <ls>Aufr. in Ku. Zeitschr. 〔1,356〕</ls>
---------
?
; <L>10713<pc>1669<k1>hu<k2>hu
; old: <ls>Aufr. in Ku. Zeitschr.&#xA0;&#xA0; 〔14,268〕</ls>
; new: <ls>Aufr. in Ku. Zeitschr. 〔14,268〕</ls>
---------
?
<ls>Roth in Ku. 〔20%%,70%%〕</ls>
---------

-----------------------------------------------------------------
../temp_graab_9i.txt 
python ../updateByLine.py ../temp_graab_9h.txt ../change_9h_9gAB.txt ../temp_graab_9i.txt
66 change transactions from ../change_9h_9gAB.txt

diff ../temp_graab_9i.txt  ../temp_graab_9g_AB.txt
#  files are the same!.

cp ../temp_graab_9i.txt  ../temp_graab_10.txt
-------------------------------------------------
c:/xampp/htdocs/cologne/csl-pywork/v02/distinctfiles/gra/pywork/graauth/
revised tooltips
revise tooltips:
  Replace tooltip: c:/xampp/htdocs/cologne/csl-pywork/v02/distinctfiles/gra/pywork/graauth/
old: O. u. O.	Orient und Occident
new: Bollensen (O. u. O.	Zur Herstellung des Veda.— Bollensenʼs Article in Orient und Occident
Remove 6 lines with '&#xA0' in abbreviation.
This string (&#xA0) is not in temp_graab_10.txt
6 matches in 5 lines for "&#" in buffer: tooltip.txt
      8:Aufr. in Ku. Zeitschr.&#xA0;	Deutsche wortdeutungen. 5) sigis.— Aufrechtʼs Article in Kuhnʼs Zeitschrift
      9:Aufr. in Ku. Zeitschr.&#xA0;&#xA0;	Etymologien.— Aufrechtʼs Article in Kuhnʼs Zeitschrift
     14:Aufrecht in Kuhn's Zeitschr.&#xA0;	Auhns.— Aufrechtʼs Article in Kuhnʼs Zeitschrift
     81:Ku. in Zeitschr.&#xA0;	Kuhnʼs two Articles in Kuhnʼs Zeitschrift

---------------------------------------------------------
cd ../
# redo.sh now uses version 10
sh redo.sh
python /c/xampp/htdocs/cologne/xmlvalidate.py dev10/pywork/gra.xml dev10/pywork/gra.dtd
# ok
---------------------------------------------------------
