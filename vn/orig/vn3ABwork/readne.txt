
Compare vn3.1_AB.txt vn3.1_AB.update.txt

python diffexamine.py vn3.1_AB.txt vn3.1_AB.update.txt diffexamine.txt

757 read from vn3.1_AB.txt
757 read from vn3.1_AB.update.txt

69 remaining differences written to diffexamine.txt
-------
cp vn3.1_AB.update.txt vn3.1_AB.update_ejf.txt
change '. N' to '.N' before :  (in the page,line section)
  39 changes

python diffexamine.py vn3.1_AB.txt vn3.1_AB.update_ejf.txt diffexamine_ejf.txt
36 remaining differences written to diffexamine_ejf.txt
  These are the remaining 'real' changes
--------------------------------------------------------

compare vn3_1.txt with vn3.1_AB.update_ejf.txt
  comparison only through first 757 lines

cp ../vn3_1.txt vn3_1_cd.txt
remove ending lines (from [Page1749] through end

python diffexamine2.py vn3_1_cd.txt vn3.1_AB.update_ejf.txt diffexamine2.txt
757 read from vn3_1_cd.txt
757 read from vn3.1_AB.update_ejf.txt
59 remaining differences written to diffexamine2.txt

#  vn3_1_cd_update.txt and vn3.1_AB.update_ejf_1.txt
cp vn3_1_cd.txt  vn3_1_cd_update.txt
cp vn3.1_AB.update_ejf.txt vn3.1_AB.update_ejf_1.txt
# manual edits of  vn3_1_cd_update.txt:
1. <cx -> <c  (1) (temporary markup not needed)
   <cy -> <c  (2) (temporary markup not needed)
2. ;  "st. anti" -> "st. -anti"  (AB)
   change to blank line
3. ; <d 287> 149,20,21 is print error in vn.
   change to blank line
4. ; VN print has 5113 (an error) (AB)
   change to blank line
----
# manual update of vn3.1_AB.update_ejf_1.txt

1. Remove ;; comments
  <c 100> <p>393,21.a v. u.: -ánti    ::AB:: st. -anti ;; print error anti for -anti ?  
  <c 147> <p>742,15: bṛ́haspátim    ::AB:: st. agním ;; print error <p>342 instead of <p>742!!
  <c 169> <p>991,15.b: -āmahe    ::AB:: st. -āmahaí ;;(e-roof) -> aí
  <c 270> <p>1513,17 v. u.: -ásya    ::AB:: st. -asya ;;print error <p>5113 instead of <p>1513!!
  <d 287> <p>149,20.21.a: pári bis {61,8} ;;print error 20,21 instead of 20. 21
  <d 341a> <p>1051,9.10: * ;;print error 1051. 9 instead of 1051,9

python diffexamine2.py vn3_1_cd_update.txt vn3.1_AB.update_ejf_1.txt diffexamine2_update.txt
50 remaining differences written to diffexamine2_update.txt

-----------------------------------------------------------
