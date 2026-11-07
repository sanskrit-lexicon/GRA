file=$1
cd ../tempgradisp || exit 1
rm -r downloads
cd ../
zip="temp_$file.zip"
cmd="zip -q -r $zip tempgradisp"
pwd
echo $cmd
$cmd
du -sh $zip 

