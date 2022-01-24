from json_explorer import main
from time import time
import cProfile, pstats, io, os
from pstats import SortKey

if __name__ == "__main__":
    os.chdir('..')  # use or not, depending on what you set your workdir to
    pr = cProfile.Profile()
    pr.enable()
    t0 = time()
    main()
    pr.disable()
    print(time() - t0)
    s = io.StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats(SortKey.CUMULATIVE)
    ps.print_stats()
    print(s.getvalue())
