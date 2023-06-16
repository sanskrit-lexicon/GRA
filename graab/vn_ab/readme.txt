AB versions of VN material
Files uploaded by VN (links to these appear in various recent issues of GRA)
.gitignore : do not track these
vn5_AB.txt  changes and deletions: L=11001 - L=11365
vn3.2_AB.updated.txt  additions:   L=12001 - L=12701
vn3.3_AB.done.txt     additional VN material appearing after the additions.
                 Not used in displays.

vn_ab/temp_vn_ab.txt  # concatenation of the above.
cat vn5_AB.txt vn3.2_AB.updated.txt vn3.3_AB.done.txt > temp_vn_ab.txt
 (note revised below)

NOTE re vn3.2_AB.updated.txt
Ref: https://github.com/sanskrit-lexicon/GRA/issues/28#issuecomment-1576066895
[Note: In my final version, couple of metaline data got changed to match my add header & hope it would not affect Jim's search results, wherein he apparently had the metaline (k1, k2) set matching in vn6 and main texts.]
See discussion in ../meta_compare/readme.txt
---------------------------------------------------------
python vn5_AB_a.py vn5_AB.txt vn5_AB_a.txt
 Manual changes for some markup.

272 ' st. ' -> ' <ab n="statt">st.</ab> '
176 ' v. u.:' -> ' <ab n="von unten">v. u.</ab>:'
1487 lines written to vn5_AB_a.txt

---------------------------------------------------------
cat vn5_AB_a.txt vn3.2_AB.updated.txt vn3.3_AB.done.txt > temp_vn_ab_a.txt
