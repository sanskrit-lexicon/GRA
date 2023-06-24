sfx="7"
file=temp_graab_$sfx.txt
origgra=/c/xampp/htdocs/cologne/csl-orig/v02/gra/gra.txt
echo "Copy $file to $origgra"
cp $file $origgra
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

echo "restoring $origgra"
cd /c/xampp/htdocs/cologne/csl-orig/v02/gra/
git restore gra.txt

