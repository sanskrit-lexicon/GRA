Begun 6-19-2023.
Refer https://github.com/sanskrit-lexicon/GRA/issues/29 comments
 following temp_graab_5 upload.
 also see https://github.com/sanskrit-lexicon/GRA/issues/30, which
  is a continuation of issue 29. Similarly at #31
NOTE(jim): 06-23-2023.  I think Andhrabharati took into account
  all of the following observations in his temp_graab_6.AB.
--------------------------------------------------------------
1. Beitr 7,252.  Beigrage Band 7,253
--------------------------------------------------------------
2.
error in the VN add section in your graab_5 file;
while generating the meta-lines for the entries,
wherever [Pagexxxx] is present without a blank line next,
all the further entries are put under the previous pc-number. [As the meta-line pc number is wrong, I happened to notice the error.]

This is seen for entries in pp. 1752-3 (as 1751), pp. 1755-6 (as 1754), pp. 1758-9 (as 1757), pp. 1764-5 (as 1763) and p.1767 (as 1766)

However, such error is not there in the previous VN portion (del & chg) of data.
Example: L=12104  pc = 1751 correct
  but L=12105 pc=1751 is wrong,  and many following
  
--------------------------------------------------------------
3. Some abbr. expansions contained a space at the end (within the quotes)--

dopp.:doppeltem :2
Gegens.:Gegensatz :19
Opt.:Optativ :157 ;; this made the singleton "Optativ" (without a space at the end) as a local abbr.!!
Optat.:Optativ :1

And in the add section that I took up at the end for markup (after a long gap) some carelessness crept in, wherein I had marked 4 entities badly, that turned up as local in your work their being different from the others--

f.:feminium:31 ;; should've been femininum
Part.:Participum:84 ;; should've been Participium
Part.:Perfektum:24 ;; should've been Perf.
pass.:passiv:2 ;; should've been passivisch
Pass.:Passiv:5 ;; should've been Passivisch

--------------------------------------------------------------
4.
While matching the markings wrt to your graab_5, noted that AV tagging is not done for the "numerals string" after the semi-colon.

Line 17652: <ls>AV. 9,3,20</ls>; {14,1,57}.
Line 58890: <ls>AV. 8,7,24</ls>; {11,1,2}.
Line 78400: <ls>AV. 4,16,1</ls>; {7,108,1}
Seen that AV. 11,1,2 has nothing related to vayas (rather वयां॑सि), but 11,2,24 has. Could this be taken as a print error?

And while checking this, noted an error in Devanagari text at 11,1,5 and posted the matter in another issue here.
--------------------------------------------------------------
5.
I took your combined file extract_ls.txt, as I felt it is more appropriate to change some of the entities as local from global.

Also noticed some corrections, while marking the ls-expansions.

--------------------------------------------------------------
6.
4 of the SV citations have a different numbering (without comma separation) while 31 have the regular numbering and 169 have no numbering at all.

We may think of inserting the commas. to make all the citation numbers in same 'style'--

<ls>SV.</ls> 〔13142〕 -> <ls>SV.</ls> 〔1,3,1,4,2〕
<ls>SV.</ls> 〔13249〕 -> <ls>SV.</ls> 〔1,3,2,4,9〕
<ls>SV.</ls> 〔13256〕 -> <ls>SV.</ls> 〔1,3,2,5,6〕
<ls>SV.</ls> 〔14141〕 -> <ls>SV.</ls> 〔1,4,1,4,1〕
--------------------------------------------------------------
7.
There are 6 entries which aren't ls-candidates strictly--

Bollensen's Conjectur	:[Bollensenʼs Conjecture]	:1
BR.'s Conjectur	:[BR.ʼs Conjecture]	:1
BR.'s Vermuthung	:[BR.ʼs guess]	:2
Lesart bei Aufr.	:[Reading in Aufrecht edition]	:1
Roth's Conjectur	:[Rothʼs Conjecture]	:1
Roth's Erläuterungen	:[Rothʼs explanations]	:1
Should these be untagged?

--------------------------------------------------------------
8. While there are 297 >BR.<, 5 places have a space in between (>B. R.<).

Can the space be removed at these 5 places, to make all the items uniform?
--------------------------------------------------------------
9. one item has a spelling correction
Deutschen Pflanzennamen -> Deutsche Pflanzennamen (and gets merged with the other one)

and another item has a portion untagged
Laute Ku. -> Ku. (and gets merged with the other one)

--------------------------------------------------------------
10. ref issue 30
  Proofreading Devanagari in
  त्रेधा॒ भागो॒ नि॒हितो यः॒ पुरा॒ वो देवा॒नां पितृ̄णां॒ म॒र्त्यानाम् ।
--------------------------------------------------------------
11. litsrc1.  (from issue 31)
TODO: document markup <ls>X &nbsp;Y</ls>

--------------------------------------------------------------
--------------------------------------------------------------
--------------------------------------------------------------
