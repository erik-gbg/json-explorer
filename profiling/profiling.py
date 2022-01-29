import cProfile, pstats, io, os, sys
from pstats import SortKey
from time import time
from json_explorer import main

if __name__ == "__main__":
    print(os.getcwd())
    #os.chdir('..')  # use or not, depending on what you set your workdir to
    pr = cProfile.Profile()
    pr.enable()
    t0 = time()
    main(sys.argv)
    pr.disable()
    print(time() - t0)
    s = io.StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats(SortKey.CUMULATIVE)
    ps.print_stats()
    print(s.getvalue())
