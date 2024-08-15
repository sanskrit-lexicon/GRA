gra="../temp_gra_0.txt"
grax="temp_gra_hwextra.txt"
python multik2.py ${gra} multik2.txt
python multik2a.py multik2.txt multik2a.txt
python make_hwextra.py multik2a.txt ${grax}
