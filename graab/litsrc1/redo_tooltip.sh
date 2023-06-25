cat extract_ls1d_AB.txt extract_ls3_local.txt > extract_ls_all.txt
python make_graauth_tooltip_2.py extract_ls_all.txt temp_tooltip.txt
cp temp_tooltip.txt /c/xampp/htdocs/cologne/csl-pywork/v02/distinctfiles/gra/pywork/graauth/tooltip.txt
wc -l extract_ls_all.txt
grep -E '^;' extract_ls_all.txt
