05-23-2023
Ref: https://github.com/sanskrit-lexicon/GRA/issues/21#issuecomment-1559865738

gra_CSL_AB_meta.head.txt is from AB, and has format
 metaline<tab>head
 
Objective Example:
OLD:
<L>25<pc>0004<k1>akutra<k2>a-ku/tra	{@a-kútra,@} {@a-kútrā.@}¦
NEW
<L>25<pc>0004<k1>akutra<k2>a-ku/tra,a-ku/trA	{@a-kútra,@} {@a-kútrā.@}¦

864 matches for "{@.*{@" in buffer: gra_CSL_AB_meta.head.txt
In 18 of these, there are 3 : {@.*{@.*{@.  None have fourt

Some have <hom>
check_1:
9940 entries have 1 {@X@} in head
 846 entries have 2 {@X@} in head
  18 entries have 3 {@X@} in head
  (+ 9940 846 18) 10804 = #  of lines in gra_CSL_AB_meta.head.txt
1 9940  no change to meta for these
2 846   change meta
3 18    change meta

41 matches for "[^}]¦" in buffer: gra_CSL_AB_meta.head.txt
  Most of these seem to need 2 headwords -- but k2 is not changed
    since there is only 1 {@X@}.

gra_CSL_AB_meta.head_1.txt
158 matches for "\\" in buffer: gra_CSL_AB_meta.head.txt
  Change these to '^'  (example: a-kuDrya\c -> a-kuDrya^c
  Since we assume Grassman's grave accent indicates 'svarita' sanskrit accent,
  and should be change to slp1 '^' -- this is consistent with MW


------------------------------------------------------------------------
## revk2_changes.txt: generate the changes
python revisek2.py gra_CSL_AB_meta.head_1.txt revk2_changes.txt
insert_newk2s warning <L>5151<pc>0758<k1>nyokas<k2>nyokas
insert_newk2s warning <L>10419<pc>1628<k1>svaBISu<k2>svaBISu/,
insert_newk2s warning <L>10487<pc>1636<k1>svastidA<k2>svasti-dA/,
insert_newk2s warning <L>10507<pc>1637<k1>svABU<k2>svABU/,
insert_newk2s warning <L>10510<pc>1638<k1>svAyuDa<k2>svAyuDa/,
864 changes written to file revk2_changes.txt
5 warnings to check

## gra_CSL_AB_meta.head_revk2.txt:  The revised file, with k2 now agreeing with that implied by the 'head'.
python ../updateByLine.py  gra_CSL_AB_meta.head_1.txt revk2_changes.txt gra_CSL_AB_meta.head_revk2.txt

