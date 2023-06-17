There are several elements in graab which are similar to the '<ab>' tag in that
they need tooltips.

ab : <ab>X</ab>   tooltip found in csl-pywork/.../graab_input.txt
     <ab n="tooltip">X</ab>  'local' tooltip
     Note: in graab_3.txt, only the '<ab n="tooltip">X</ab>' form appears.
     TODO: for 'most' (but not all) of these,
       a) coordinate graab_input.txt
       b) replace with first form (<ab>X</ab>)
pe : [Person] Some 'local' and some 'global'
      'global' ('<pe>X</pe>'  
      see GRA.pe.tags.txt for global tooltips
      Displays access global tooltips from graab_input.txt
lang : [language name] : Most global. 1 local.
    GRA.lang.tags.with.expansion.done.txt has tooltips
      Displays access global tooltips from graab_input.txt
  NOTE:   GRA.lang.tags.with.expansion.txt is almost same.
  REF: https://github.com/sanskrit-lexicon/GRA/issues/29#issuecomment-1590320226
  diff ~/Downloads/gra/GRA.lang.tags.with.expansion.txt ~/Downloads/gra/GRA.lang.tags.with.expansion.done.txt
19c19
< <lang>angels.</lang>  English
---
> <lang>angels.</lang>  Anglo-Saxon
24a25
> <lang>germ.</lang>    German
31a33
> <lang>hzv.</lang>     Middle Persian/Pahlavi ('Huzvaresh' script)
41c43
< <lang>ndd.</lang>     ???
---
> <lang>ndd.</lang>     Low German
47d48
< <lang>prät.</lang>    Should've been as <ab>prät.</ab> Präteritum (Simple Past tense)
51a53
> <lang>skt.</lang>     Sanskrit

------------------------------------------------
local copy of graab_input.txt  (GRA abbreviation tooltip file)
cp /c/xampp/htdocs/cologne/csl-pywork/v02/distinctfiles/gra/pywork/graab/graab_input.txt graab_input.txt
------------------------------------------------

python extract_abbrev.py ../temp_graab_3.txt extract_abbrev.txt extract_abbrev_local.txt

------------------------------------------------
Change markup for the 'global' abbreviations (those in extract_abbrev.txt).
Example: <ab n="adjektiv">a.</ab> -> <ab>a.</ab>
python global_ab.py ../temp_graab_3.txt extract_abbrev.txt ../temp_graab_4.txt

89186 from ../temp_graab_3.txt
279 abbreviations read from extract_abbrev.txt
change_lines: 26018 lines changed
89186 lines written to temp_graab_4a.txt
checking global abbreviations
   0 problems with abbreviations
-----------------------------------------------
'pe' abbreviations
See GRA.pe.tags.txt

extract_pe.txt
Same format as extract_abbrev.txt
1.:1sten/ersten:1
2.:2ten/zweiten:1
3.:3ten/dritten:3

------------------------------------------------------------------
lang abbreviations
Cf. GRA.lang.tags.with.expansion.done.txt

No changes required for 
Generate extract_lang.txt, in same format as extract_abbrev.txt
and get counts from ../temp_graab_4.txt

python extract_lang.py ../temp_graab_4.txt GRA.lang.tags.with.expansion.done.txt extract_lang.txt 
Note: changed apostrophes to left/right single quote
   'Huzvaresh' -> ‘Huzvaresh’).
   Reason: compatibility with CDSL display logic for abbreviations

89186 lines from ../temp_graab_4.txt
59 records parsed from GRA.lang.tags.with.expansion.done.txt
481 lang tags found
59 lines written to extract_lang.txt
---------------------------------------------------------------

python prepare_ls.py ../temp_graab_4.txt extract_ls0.txt extract_ls0_local.txt
NOTE: moved to litsrc directory
---------------------------------------------------------------
rename the old abbreviation file:
mv graab_input.txt graab_input_old.txt
---------------------------------------------------------------
construct new version of abbreviation file from
1. concatenate
 cat extract_abbrev.txt extract_lang.txt extract_pe.txt > temp_extract_all.txt
2. Construct graab_input.txt, the new abbreviation file
python make_graab_input.py temp_extract_all.txt graab_input.txt
341 abbreviations read from temp_extract_all.txt
341 lines written to graab_input.txt

--------------------------------------------------------
