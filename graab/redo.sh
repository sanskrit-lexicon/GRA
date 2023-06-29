sfx="9"
file=temp_graab_$sfx.txt
filex=gra_hwextra.txt
origdir=/c/xampp/htdocs/cologne/csl-orig/v02/gra
origgra=$origdir/gra.txt
origx=$origdir/$filex
echo "Copy $file to $origgra"
cp $file $origgra
echo "Copy $filex to $origx"
cp $filex $origx
echo
devdir=/c/xampp/htdocs/sanskrit-lexicon/GRA/graab/dev$sfx
echo "BEGIN Generate display in $devdir"
echo "-------------------------------------------------"
cd /c/xampp/htdocs/cologne/csl-pywork/v02/
root=dev_$sfx
echo
pwd
sh generate_dict.sh gra $devdir
echo
echo "EBD generate display in $devdir"
echo "-------------------------------------------------"

cd /c/xampp/htdocs/cologne/csl-orig/v02/gra/
echo "restoring $origgra"
git restore gra.txt
echo "restoring $origx"
git restore $filex

