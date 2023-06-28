# literary source markup work based on ../temp_graab_7.txt

See issue31

------------------------------------------------------------
python rvlinks_nonstandard.py ../temp_graab_7.txt rvlinks_nonstandard.txt

113486 standard rvlinks, 5231 non-standard
4176 distinct non-standard

standard form: {X,Y} where X and Y are digit sequences
non-standard: {DZ} where D is a digit and Z does not contain '}'

------------------------------------------------------------
reformat the non-standard rvlinks.
python reform.py rvlinks_nonstandard.txt reform_1.txt


------------------------------------------------------------
../temp_graab_8a.txt
apply reform_1.
For the remaining '?' items, mark as ?_{
python apply_reform.py ../temp_graab_7.txt reform_1.txt ../temp_graab_8a.txt

89186 read from ../temp_graab_7.txt
4176 non-standard rvlinks read from reform_1.txt
apply_reform changes 2545 lines
89186 lines written to ../temp_graab_8a.txt
0 unused rvlinks

311 matches in 257 lines for "?_" in buffer: temp_graab_8a.txt  

------------------------------------------------------------
../temp_graab_8b.txt

cp ../temp_graab_8a.txt ../temp_graab_8b.txt
  Manually correct the ?_{ cases, and leave corrected as _?{
------------------------------------------------------------
Todo: <ab n="Vorige">V.</ab> ?_{992,5}
new? <ab n="Vers">V.</ab> ?_{992,5}
------------------------------------------------------------
python rvlinks_nonstandard.py ../temp_graab_8b.txt temp_rvlinks_nonstandard_1.txt
124901 standard rvlinks, 0 non-standard
0 distinct non-standard
0 lines written to temp_rvlinks_nonstandard_1.txt

------------------------------------------------------------
python ../diff_to_changes_dict.py ../temp_graab_8a.txt ../temp_graab_8b.txt change_8a_8b.txt
257 changes written to change_8a_8b.txt

------------------------------------------------------------
sh redo_7_8b.txt
Reconstructs temp_redo_graab_8b.txt from ../temp_graab_7.txt
This 
------------------------------------------------------------
cp ../temp_graab_8b.txt ../temp_graab_8.txt
python 
------------------------------------------------------------
------------------------------------------------------------
------------------------------------------------------------
