litsrc/readme.txt

Work with <ls> tag.
This appears primarily in the form <ls>X</ls>
 A few are 'local': <ls n="A">X</ls> 

extract_ls0.txt extract_ls0_local.txt show these instances.

python prepare_ls.py ../temp_graab_4.txt extract_ls0.txt extract_ls0_local.txt
89186 lines from ../temp_graab_4.txt
129 global ls tags
2272 ls tag instances found
129 lines written to extract_ls0.txt
10 local ls tags
35 local ls tag instances found
10 lines written to extract_ls0_local.txt


Regarding local abbreviations:
-  <ls n="Pada">P.</ls> appears 25 times.
-  9 other abbreviations appear total of 10 times in local form.

There is no overlap in ls abbreviations between the global and local.
  Thus, no need for the 'local' forms.

-----------------------------------------------
../temp_graab_5a.txt  all ls local
Change local abbreviation markup to global form
<ls n="T">X</ls> -> <ls>X</ls>
python make_5a.py ../temp_graab_4.txt ../temp_graab_5a.txt

-----------------------------------------------
temp_graab_5b
 <ls>AV.</ls> {a,b,c} -> <ls>AV. a,b,c</ls>
 So displays will have link-target for Atharva Veda.
python make_5b.py ../temp_graab_5a.txt ../temp_graab_5b.txt
-----------------------------------------------
temp_graab_5c
 There are still some 'extra' AV links.
11 matches for "<ls>AV.</ls> {" in buffer: temp_graab_5b.txt
Example: <ls>AV.</ls> {2,27,1. 7}

cp ../temp_graab_5b.txt ../temp_graab_5c.txt

Manually edit 5c
-----------------------------------------------
python prepare_ls.py ../temp_graab_5a.txt extract_ls.txt temp_extract_ls_local.txt
139 global ls tags
2307 ls tag instances found
139 lines written to extract_ls.txt
0 local ls tags
-----------------------------------------------
csl-pywork/v02
1. modify inventory.txt
ben ap90 sch gra:pywork/${dictlo}auth/redo.sh:CD
ben ap90 sch gra:pywork/${dictlo}auth/readme.org:CD
ben ap90 sch gra:pywork/${dictlo}auth/tooltip.txt:CD
ben ap90 sch gra:pywork/${dictlo}auth/tooltips.sql:CD
2.modify makotemplates/pywork/redo_postxml.sh

# literary source.
%if dictlo in ['mw','pw','pwg','ap90','ben','pwkvn','sch','gra']:
 cd ${dictlo}auth
 sh redo.sh
 cd ../ # back to pywork
%endif
3. initialize distinctfiles/gra/pywork/graauth  directory
3a. Copy distinctfiles/ben/pywork/benauth to
         distinctfiles/gra/pywork/graauth
3b. edit files in graauth - change ben to gra
   readme.org, redo.sh, tooltips.sql
3c. tooltips.txt has format
 abbrev<TAB>tip
-----------------------------------------------
temp_tooltips.txt
Simple change of format
python make_graauth_tooltip.py extract_ls.txt temp_tooltips.txt

# manually edit for testing. 
temp_tooltips_test.txt
# upload to csl-pywork
cp temp_tooltips_test.txt /c/xampp/htdocs/cologne/csl-pywork/v02/distinctfiles/gra/pywork/graauth/tooltip.txt
