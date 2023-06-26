06-25-2023
Reexamine abbreviations (ab, pe, lang)
begin with ../temp_graab_7e.txt

There are several elements in graab which are similar to the '<ab>' tag in that
they need tooltips.

ab : <ab>X</ab>   tooltip found in csl-pywork/.../graab_input.txt
     <ab n="tooltip">X</ab>  'local' tooltip
pe : [Person] Some 'local' and some 'global'
      'global' '<pe>X</pe>'  
      Displays access global tooltips from graab_input.txt
lang : [language name] : Most global. 1 local.
;    ../abbrevs/GRA.lang.tags.with.expansion.done.txt has tooltips
      Displays access global tooltips from graab_input.txt

------------------------------------------------
local copy of graab_input.txt  (GRA abbreviation tooltip file)
cp /c/xampp/htdocs/cologne/csl-pywork/v02/distinctfiles/gra/pywork/graab/graab_input.txt graab_input_0.txt
------------------------------------------------
extract_abbrev.txt
tab-separated fields
 tag  ab,pe,lang
 type lo, gl   local or global
 abbrev - the abbreviation
 count - number of instances (of abbrev+tip)
 tip - from graab_input_0.txt for global; as written for local

python extract_abbrev.py ../temp_graab_7e.txt graab_input_0.txt extract_abbrev.txt

341 global abbreviations read from graab_input_0.txt   (0 duplicates)
365 lines written to extract_abbrev.txt
040 ab,local
251 ab,global
003 pe,local
003 pe,global
001 lang,local
058 lang,global
--------------------------------------------------------------------
../change_7f.txt
⁓ -> <ab>⁓</ab>  (two instances)

python ../updateByLine.py ../temp_graab_7e.txt ../change_7f.txt ../temp_graab_7f.txt
cp ../temp_graab_7f.txt ../temp_graab_7.txt
--------------------------------------------------------------------
cp graab_input_0.txt graab_input_1.txt
edit graab_input_1.txt
 1) add
   ⁓	<id>⁓</id> <disp>at similar; at identical, parallel passages</disp>
 2) change
 Ref: https://github.com/sanskrit-lexicon/GRA/issues/31#issuecomment-1606251248
 old:
zd.	<id>zd.</id> <disp>Zend</disp>
Zend	<id>Zend</id> <disp>Zend</disp>
Zend.	<id>Zend.</id> <disp>Zend</disp>
zend.	<id>zend.</id> <disp>Zend</disp>
 new:
zd.	<id>zd.</id> <disp>Zend (Avestan)</disp>
Zend	<id>Zend</id> <disp>Zend (Avestan)</disp>
Zend.	<id>Zend.</id> <disp>Zend (Avestan)</disp>
zend.	<id>zend.</id> <disp>Zend (Avestan)</disp>
---------------------------------------------
python extract_abbrev.py ../temp_graab_7f.txt graab_input_1.txt extract_abbrev_1.txt

342 global abbreviations read from graab_input_1.txt   (0 duplicates)
366 lines written to extract_abbrev.txt
040 ab,local
252 ab,global
003 pe,local
003 pe,global
001 lang,local
058 lang,global
---------------------------------------------
graab_input_2.txt
 Remove unused global abbreviations
python extract_abbrev1.py ../temp_graab_7f.txt graab_input_1.txt temp_extract_abbrev_1.txt graab_input_2.txt
 NOTE: diff extract_abbrev_1.txt temp_extract_abbrev_1.txt  (NO DIFFERENCE)

342 global abbreviations read from graab_input_1.txt   (0 duplicates)
366 lines written to temp_extract_abbrev_1.txt
040 ab,local
252 ab,global
003 pe,local
003 pe,global
001 lang,local
058 lang,global
dglab unused: Ait.      <id>Ait.</id> <disp>Aiton</disp>
dglab unused: antreff.  <id>antreff.</id> <disp>antreffen</disp>
dglab unused: Bharadv.  <id>Bharadv.</id> <disp>Bharadvāja</disp>
dglab unused: Brahmanasp.       <id>Brahmanasp.</id> <disp>Brahmanaspati</disp>
dglab unused: bṛ́hasp.  <id>bṛ́hasp.</id> <disp>bṛ́haspátim</disp>
dglab unused: Citr.     <id>Citr.</id> <disp>Citráratha</disp>
dglab unused: Dsch.     <id>Dsch.</id> <disp>Dschamadagni</disp>
dglab unused: germ.     <id>germ.</id> <disp>German</disp>
dglab unused: Gm.       <id>Gm.</id> <disp>Gmelin</disp>
dglab unused: Gärtn.    <id>Gärtn.</id> <disp>Gärtner</disp>
dglab unused: H.        <id>H.</id> <disp>Himmel</disp>
dglab unused: Hymn.     <id>Hymn.</id> <disp>Hymne</disp>
dglab unused: K.        <id>K.</id> <disp>Karañja</disp>
dglab unused: Lam.      <id>Lam.</id> <disp>Lamarck</disp>
dglab unused: Lin.      <id>Lin.</id> <disp>Linnaeus</disp>
dglab unused: M.        <id>M.</id> <disp>Mātaríśva</disp>
dglab unused: Mitr.     <id>Mitr.</id> <disp>Mitra</disp>
dglab unused: ms.       <id>ms.</id> <disp>manuscriptum</disp>
dglab unused: pp.       <id>pp.</id> <disp>perge, perge‎</disp>
dglab unused: Pr.       <id>Pr.</id> <disp>Priyamedha</disp>
dglab unused: R. Br.    <id>R. Br.</id> <disp>Robert Brown</disp>
dglab unused: Rich.     <id>Rich.</id> <disp>Richard</disp>
dglab unused: Roxb.     <id>Roxb.</id> <disp>Roxburghii</disp>
dglab unused: St.       <id>St.</id> <disp>Stamm</disp>
dglab unused: Sth.      <id>Sth.</id> <disp>Sthūragūpa</disp>
dglab unused: utt.      <id>utt.</id> <disp>uttama</disp>
dglab unused: W.        <id>W.</id> <disp>Wetterwolke</disp>
dglab unused: Willd.    <id>Willd.</id> <disp>Willdenow</disp>
dglab unused: Y.        <id>Y.</id> <disp>Yayāti</disp>
29 dglab records unused
313 lines written to graab_input_2.txt

---------------------------------------------
python extract_abbrev1.py ../temp_graab_7f.txt graab_input_2.txt temp_extract_abbrev_1.txt temp_graab_input_3.txt
313 global abbreviations read from graab_input_2.txt   (0 duplicates)
366 lines written to temp_extract_abbrev_1.txt
040 ab,local
252 ab,global
003 pe,local
003 pe,global
001 lang,local
058 lang,global
0 dglab records unused
313 lines written to temp_graab_input_3.txt
---------------------------------------------------------
install graab_input_2.txt (GRA abbreviation tooltip file)
cp graab_input_2.txt /c/xampp/htdocs/cologne/csl-pywork/v02/distinctfiles/gra/pywork/graab/graab_input.txt 
