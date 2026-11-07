file=$1
cp $1 ../tempgradisp/orig/gra.txt
cd ../tempgradisp || exit 1
sh redo.sh
