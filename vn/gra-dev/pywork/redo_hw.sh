echo "BEGIN redo_hw.sh"
echo "construct xxxhw.txt"
python3 hw.py ../orig/gra.txt hwextra/gra_hwextra.txt grahw.txt
python3 hw2.py grahw.txt grahw2.txt
python3 hw0.py grahw.txt grahw0.txt
# both hw2.txt and hw0.txt are easily constructed from hw.txt
# not clear, therefore, that either hw2.txt or hw0.txt is needed directly
# We would need to change the 'awork/sanhw1.pt' program. 
# To avoid this change might be sufficient reason to keep hw2.txt and hw0.txt
echo "construct xxxhw2.txt"
echo "construct xxxhw0.txt"
echo "DONE redo_hw.sh"
