echo "remake mwverbs"
python mwverb.py mw ../../mw/mw.txt mwverbs.txt
echo "remake mwverbs1"
python mwverbs1.py mwverbs.txt mwverbs1.txt
echo "remake gra_verb_filter.txt"
python gra_verb_filter.py ../gra.txt  gra_verb_exclude.txt gra_verb_include.txt gra_verb_filter.txt

echo "remake gra_verb_filter_map.txt"
python gra_verb_filter_map.py gra_verb_filter.txt mwverbs1.txt gra_verb_filter_map.txt
echo "remake gra_preverb0.txt"
python preverb0.py ../gra.txt gra_verb_filter_map.txt gra_upasarga_map.txt gra_preverb0.txt 

echo "remake gra_preverb1.txt"
python preverb1.py slp1 gra_preverb0.txt gra_verb_filter_map.txt mwverbs1.txt gra_preverb1.txt
echo "remake gra_preverb1_deva.txt"
#python preverb1.py deva ../gra.txt gra_verb_filter_map.txt mwverbs1.txt gra_preverb1_deva.txt
python preverb1.py deva gra_preverb0.txt gra_verb_filter_map.txt mwverbs1.txt gra_preverb1_deva.txt
