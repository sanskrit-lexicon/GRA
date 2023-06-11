compare meta lines.

AB comment on the 'additions (vn3.2_AB.updated.txt' see ../vn_ab/readme.txt)

```
Note: In my final version,
 couple of metaline data got changed to match my add header &
 hope it would not affect Jim's search results,
 wherein he apparently had the metaline (k1, k2)
 set matching in vn6 and main texts.]

Output:  <L>X<k1>Y  (just the L and k1 fields of metalines)
python metak1.py ../temp_gra9.txt temp_metak1_gra9.txt
11852 lines written to temp_metak1_gra9.txt

python metak1.py ../temp_graab_2.txt temp_metak1_graab_2.txt
11871 lines written to temp_metak1_graab_2.txt

diff temp_metak1_gra9.txt temp_metak1_graab_2.txt > diff_meta_gra9_graab_2.txt

See readme_diff.txt for analysis of diff_meta_gra9_graab_2.txt
