python -m cProfile -o output.pstats ./Main.py
gprof2dot -f pstats output.pstats | dot -Tpng -o profileoutput.png
