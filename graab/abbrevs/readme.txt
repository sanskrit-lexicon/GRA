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
    GRA.lang.tags.with.expansion.txt has tooltips
      Displays access global tooltips from graab_input.txt
------------------------------------------------
local copy of graab_input.txt  (GRA abbreviation tooltip file)
cp /c/xampp/htdocs/cologne/csl-pywork/v02/distinctfiles/gra/pywork/graab/graab_input.txt graab_input.txt
------------------------------------------------

python extract_abbrev.py ../temp_graab_3.txt extract_abbrev.txt extract_abbrev_local.txt

