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
