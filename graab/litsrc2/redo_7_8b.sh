python apply_reform.py ../temp_graab_7.txt reform_1.txt ../temp_graab_8a.txt

python ../updatebyLine.py ../temp_graab_8a.txt change_8a_8b.txt temp_redo_graab_8b.txt

diff ../temp_graab_8b.txt  temp_redo_graab_8b.txt | wc -l

