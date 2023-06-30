gra/graab/meta2/readme.txt
Begin 06-30-2023

----------------------------------------------------------------------
check_ea1.txt
python check_ea1.py ../temp_graab_9.txt check_ea1.txt
163 extended ascii codes found in ../temp_graab_9.txt

correction to remove two instances of "(\u200e)     2 := LEFT-TO-RIGHT MARK"
../change_9c.txt
python ../updateByline.py ../temp_graab_9b.txt ../change_9c.txt ../temp_graab_9c.txt
2 change transactions from ../change_9c.txt

cp ../temp_graab_9c.txt ../temp_graab_9.txt

Recalc check_ea1
python check_ea1.py ../temp_graab_9.txt check_ea1.txt
162 extended ascii codes found in ../temp_graab_9.txt

----------------------------------------------------------------------
