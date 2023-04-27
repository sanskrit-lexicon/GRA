
Step 1:
compare temp_gra_6.txt with Andhrabharati's temp_gra_.CSL._.AB.txt

python diff1.py ../temp_gra_6.txt temp_gra_.CSL._.AB.txt diff1.txt abbrev.txt
86245 read from ../temp_gra_6.txt
86245 read from temp_gra_.CSL._.AB.txt
7764 remaining differences written to diff1.txt

Some AB errors in
… ->  〰
377 new <div n="P1">-it {394,5} (neben mugdhás), {858,7} (… kṣetravídam hí áprāṭ).
533 new <div n="P1">-ás 1) {841,14} (yé … yé ánagnidagdhās).
746 new <div n="P1">-us [m.] {911,44} … ápatighnī edhi.
61897 new <div n="P1">-ā́sas 3) … ná yé (marútas) suajā́s svátavasas {168,2}.

probably others

5897 matches in 4471 lines for "〰" in buffer: temp_gra_6.txt
334 matches in 316 lines for "…" in buffer: temp_gra_6.txt

212 matches in 21 lines for "〰" in buffer: temp_gra_.CSL._.AB.txt
5971 matches in 4504 lines for "…" in buffer: temp_gra_.CSL._.AB.txt


AB: Don't do this:
32713 old <div n="P1">-ā́s [A. p. f.] 1) srotyā́s {AV. 10,1,16}.
  {AV. 10,1,16}  form is needed by current link target in display for GRA.
32713 new <div n="P1">-ā́s [A. p. f.] 1) srotyā́s AV. {10,1,16}.

AB: use standard ls form except for RV and AV:
 <ls>Cu.</ls> {185}  => <ls>Cu. 185</ls>
  
--------------------------------------------------------------
# exclude differences re … and  〰
python diff2.py ../temp_gra_6.txt temp_gra_.CSL._.AB.txt diff2.txt abbrev.txt
3974 remaining differences written to diff2.txt

============================================================================
Step 2:
cp temp_gra_.CSL._.AB.txt temp_gra_.CSL._.AB1.txt
manually edit temp_gra_.CSL._.AB1.txt
  … -> XXX 5971
  〰 -> …  212
  XXX -> 〰 5971

============================================================================
Step 3:
../temp_gra_7.txt

Replace certain lines of temp_gra_.CSL._.AB1.txt with corresponding
 line of temp_gra_7.
 This is done when the corresponding line of temp_gra_7 has a
  <c N>X</c> form (text to be changed).
 Note: Also, remove '<lbinfo../>'
python add_chg_AB1.py ../temp_gra_6.txt temp_gra_.CSL._.AB1.txt change_7.txt


86245 read from ../temp_gra_6.txt
86245 read from temp_gra_.CSL._.AB1.txt
264 changes written to change_7.txt

## install these changes to temp_gra_.CSL._.AB1.txt in new version
 ../temp_gra_7.txt.
python ../updateByLine.py temp_gra_.CSL._.AB1.txt change_7.txt ../temp_gra_7.txt

