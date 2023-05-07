file=$1
cd ../tempgradisp
rm -r downloads
cd ../
zip="temp_$file.zip"
cmd="zip -q -r $zip tempgradisp"
pwd
echo $cmd
$cmd
du -sh $zip 

