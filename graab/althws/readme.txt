# generate gra_hwextra.txt (alternate headwords)

See issue32


------------------------------------------------------------
python multik2.py ../temp_graab_9a.txt multik2.txt

89186 lines read from ../temp_graab_9a.txt
11871 entries found
WARNING: metaline=<L>11117<pc>1743-b<k1>jyA<k2>jyA/, jiA/<h>2
         metacalc=<L>11117<pc>1743-b<k1>jyA<k2>jyA/, jiA/
WARNING: metaline=<L>11291<pc>1747-a<k1>ah<k2>ah, aMh<h>1
         metacalc=<L>11291<pc>1747-a<k1>ah<k2>ah, aMh
WARNING: metaline=<L>11295<pc>1747-a<k1>Arya<k2>A/rya, a/ria<h>2
         metacalc=<L>11295<pc>1747-a<k1>Arya<k2>A/rya, a/ria
896 metalines with comma
896 records written to multik2.txt

../change_9b.txt
python updateByLine.py temp_graab_9a.txt change_9b.txt temp_graab_9b.txt
89186 lines read from temp_graab_9a.txt
89186 records written to temp_graab_9b.txt
6 change transactions from change_9b.txt

# rerun
python multik2.py ../temp_graab_9b.txt multik2.txt
89186 lines read from ../temp_graab_9b.txt
11871 entries found
896 metalines with comma
896 records written to multik2.txt
--------------------------------------------
multik2a.txt
# construct k1 for each k2.
# check that 1st k1 agrees with k1 of metaline.
python multik2a.py multik2.txt multik2a.txt

generate_Ls_manual: 6754.1,6755,1 -> ['6754.2']
generate_Ls_manual: 6881,6881.5,1 -> ['6881.1']
896 records written to multik2a.txt
916 extra headwords


------------------------------------------------------------
python make_hwextra.py multik2a.txt ../gra_hwextra.txt


------------------------------------------------------------
; 06-29-2023
Ref: https://github.com/sanskrit-lexicon/GRA/issues/32#issuecomment-1612416266
additional corrections in ../change_9b.txt
  at L=3458 and 7174
python ../updateByLine.py ../temp_graab_9a.txt ../change_9b.txt ../temp_graab_9b.txt
8 change transactions from change_9b.txt

cp ../temp_graab_9b.txt ../temp_graab_9.txt

python multik2.py ../temp_graab_9b.txt multik2.txt
894 records written to multik2.txt

python multik2a.py multik2.txt multik2a.txt

python make_hwextra.py multik2a.txt ../gra_hwextra.txt

------------------------------------------------------------
------------------------------------------------------------
