# 10K instructions NO VICTIM CACHE

python cacheSim.py -i gcc-10K.memtrace -cs 512 -bs 16 -w 1 -vs 0

python cacheSim.py -i gcc-10K.memtrace -cs 512 -bs 16 -w 2 -vs 0

python cacheSim.py -i gcc-10K.memtrace -cs 512 -bs 16 -w 4 -vs 0

python cacheSim.py -i gcc-10K.memtrace -cs 512 -bs 16 -w 0 -vs 0

# 1M instructions NO VICTIM CACHE

python cacheSim.py -i gcc-1M.memtrace -cs 512 -bs 16 -w 1 -vs 0

python cacheSim.py -i gcc-1M.memtrace -cs 512 -bs 16 -w 2 -vs 0

python cacheSim.py -i gcc-1M.memtrace -cs 512 -bs 16 -w 4 -vs 0

python cacheSim.py -i gcc-1M.memtrace -cs 512 -bs 16 -w 0 -vs 0

# 1M INSTRUCTIONS WITH VICTIM CACHE 4

python cacheSim.py -i gcc-1M.memtrace -cs 512 -bs 16 -w 1 -vs 4

python cacheSim.py -i gcc-1M.memtrace -cs 512 -bs 16 -w 4 -vs 4

python cacheSim.py -i gcc-1M.memtrace -cs 512 -bs 16 -w 0 -vs 4

# 1M INSTRUCTIONS WITH VICTIM CACHE 8

python cacheSim.py -i gcc-1M.memtrace -cs 512 -bs 16 -w 1 -vs 8

python cacheSim.py -i gcc-1M.memtrace -cs 512 -bs 16 -w 4 -vs 8

python cacheSim.py -i gcc-1M.memtrace -cs 512 -bs 16 -w 0 -vs 8

# 1M INSTRUCTIONS WITH VICTIM CACHE 16

python cacheSim.py -i gcc-1M.memtrace -cs 512 -bs 16 -w 1 -vs 16

python cacheSim.py -i gcc-1M.memtrace -cs 512 -bs 16 -w 4 -vs 16

python cacheSim.py -i gcc-1M.memtrace -cs 512 -bs 16 -w 0 -vs 16 
