import math
import argparse

class CacheSim:
    blockSizeList = {2, 4, 8, 16, 32, 64}
    waysList = {0, 1, 2, 4, 8, 16}
    vCacheSizeList = {0, 4, 8, 16}
    MAX_CACHE_SIZE = 4097*1024
    MIN_CACHE_SIZE = 1*1024

    inputFile = ""  # Input File
    cacheSize = 1  # Cache Size
    blockSize = 2  # Block Size
    ways = 1  # Associativity
    vCacheSize = 0  # VCS

    setsCount = 0
    linesCount = 0
    hits = 0
    misses = 0

    instructions = []
    cache = []
    victimCache = []

    def setup_simulator(self):
        inputFileName, cacheSize, blockSize, ways, vCacheSize = self.input_cache_properties()
        self.validate_inputs(blockSize, cacheSize, vCacheSize, ways)
        if ways == 0:
            self.ways = cacheSize / blockSize
            self.setsCount = 1
        else:
            self.ways = ways
            self.setsCount = cacheSize / blockSize / ways
        self.inputFile = "inputFiles/" + inputFileName
        self.cacheSize = cacheSize
        self.blockSize = blockSize
        self.linesCount = self.setsCount * ways
        self.vCacheSize = vCacheSize
        self.open_input_file()

    def run_simulator(self):
        self.initialize_cache()
        self.initialize_victim_cache()
        print("Starting Cache Simulation ...\n")
        for instruction in self.instructions:
            index, tag = self.resolve_address(instruction)
            self.find_in_cache(self.cache, index, tag)
        print "Cache Simulation Complete ...\n"

    def find_in_cache(self, cache, index, tag):
        for cache_set in range(self.setsCount):
            if cache[cache_set]["index"] == index:
                for line in range(self.ways):
                    if cache[cache_set]["lines"][line]["tag"] == tag:
                        self.hits += 1
                        usedLine = cache[cache_set]["lines"][line]
                        cache[cache_set]["lines"].pop(line)
                        cache[cache_set]["lines"].insert(0, usedLine)
                        usedSet = cache[cache_set]
                        cache.pop(cache_set)
                        cache.insert(0, usedSet)
                        return
                self.misses += 1
                self.victim_cache_check(self.victimCache, index, tag)
                newLine = self.new_cache_line(tag)
                lru_Line = cache[cache_set]["lines"].pop()
                self.victim_cache_push(index, lru_Line["tag"])
                cache[cache_set]["lines"].insert(0, newLine)
                usedSet = cache[cache_set]
                cache.pop(cache_set)
                cache.insert(0, usedSet)
                return
        self.misses += 1
        self.victim_cache_check(self.victimCache, index, tag)
        newSet = self.new_cache_set(index, tag)
        lru_Set = cache.pop()
        self.victim_cache_push_set(lru_Set)
        cache.insert(0, newSet)
        return

    def new_cache_set(self, index, tag):
        cacheSet = {}
        cacheSet["index"] = index
        cacheSet["lines"] = []
        for line in range(self.ways):
            cacheSet["lines"].insert(line, self.new_cache_line(0))
        cacheSet["lines"][0]["tag"] = tag
        return cacheSet

    def new_cache_line(self, tag):
        line = {}
        line["tag"] = tag
        return line

    def victim_cache_check(self, victimCache, index, tag):
        if self.vCacheSize == 0:
            return False
        for vLine in range(len(victimCache)):
            vCacheLine = victimCache[vLine]
            if vCacheLine["index"] == index:
                if vCacheLine["tag"] == tag:
                    self.misses -= 1
                    self.hits += 1
                    vCacheLine = victimCache.pop(vLine)
                    victimCache.append(vCacheLine)
                    return True

    def victim_cache_push(self, index, tag):
        if self.vCacheSize == 0:
            return
        vCacheLine = {}
        vCacheLine["index"] = index
        vCacheLine["tag"] = tag
        self.victimCache.pop()
        self.victimCache.insert(0, vCacheLine)

    def victim_cache_push_set(self, lru_set):
        line = 0
        while (line < self.vCacheSize) and (line < len(lru_set["lines"])):
            self.victim_cache_push(lru_set["index"], lru_set["lines"][line]["tag"])
            line += 1

    def input_cache_properties(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("-i", "--i", help="inputFileName", type=str)
        parser.add_argument("-cs", "--cs", help="cacheSize", type=int)
        parser.add_argument("-bs", "--bs", help="blockSize", type=int)
        parser.add_argument("-w", "--w", help="ways", type=int)
        parser.add_argument("-vs", "--vs", help="victimCacheSize", type=int)
        args = parser.parse_args()
        i = args.i
        cs = args.cs * 1024
        bs = args.bs
        w = args.w
        vcs = args.vs
        return i, cs, bs, w, vcs

    def validate_inputs(self, blockSize, cacheSize, vCacheSize, ways):
        if cacheSize not in range(self.MIN_CACHE_SIZE, self.MAX_CACHE_SIZE):
            print "Incorrect Input CS %s" % cacheSize
            exit(-1)
        if blockSize not in self.blockSizeList:
            print "Incorrect Input BS"
            exit(-1)
        if ways not in self.waysList:
            print "Incorrect Input ways"
            exit(-1)
        if vCacheSize not in self.vCacheSizeList:
            print "Incorrect Input VCS"
            exit(-1)

    def open_input_file(self):
        print "\nReading %s ...\n" % self.inputFile
        with open(self.inputFile) as content:
            self.instructions = content.readlines()

    def initialize_cache(self):
        if self.ways == (self.cacheSize / self.blockSize):
            mapping = "fully-associative"
        elif self.ways == 1:
            mapping = "direct-mapped"
        else:
            mapping = str(self.ways) + "-way set associative"
        print "Initializing %s Cache of %s KB ...\n" % (mapping,
                                                        (self.cacheSize) / 1024)
        for set in range(self.setsCount):
            self.cache.insert(set, self.new_cache_set(0, 0))
        print "**Initialization complete**\n"

    def initialize_victim_cache(self):
        if self.vCacheSize == 0:
            print("No Victim Cache ...")
            return
        print "Initializing Victim Cache of size %d ...\n" % self.vCacheSize
        for vLine in range(self.vCacheSize):
            vCacheLine = {}
            vCacheLine["index"] = 0
            vCacheLine["tag"] = 0
            self.victimCache.insert(vLine, vCacheLine)
        print "*** Victim Cache Initialization Complete ***"

    def resolve_address(self, instruction):
        address = int(instruction.split()[2], 16)
        offset = int(instruction.split()[1])
        address = address + offset
        address %= (2 ** 32)
        index = address >> int(math.log(self.blockSize, 2))
        index %= self.setsCount
        tag = address >> int(math.log(self.setsCount, 2) +
                             math.log(self.blockSize, 2))
        return index, tag

    def address_structure(self):
        offset_bits = int(math.log(self.blockSize, 2))
        index_bits = int(math.log(self.setsCount, 2))
        tag_bits = 32 - offset_bits - index_bits
        return index_bits, offset_bits, tag_bits

    def display_results(self):
        index_bits, offset_bits, tag_bits = self.address_structure()
        address_format = [
            ["Tag", "Index", "Offset"],
            [tag_bits, index_bits, offset_bits]
        ]
        print("Instructions     %d") % len(self.instructions)
        print("SETS             %d") % self.setsCount
        print("WAYS             %d") % self.ways
        if self.vCacheSize != 0:
            print("VCacheSize       %d") % self.vCacheSize
        print("TAG BITS         %d") % tag_bits
        print("INDEX BITS       %d") % index_bits
        print("OFFSET BITS      %d") % offset_bits
        print("MISSES           %d") % self.misses
        print("HITS             %d") % self.hits
        missRate = (self.misses * 100.0) / len(self.instructions)
        print("MISS-RATE        %f") % missRate
        print("HIT-RATE         %f") % (100.0 - missRate)


def main():
    cacheSim = CacheSim()
    cacheSim.setup_simulator()
    cacheSim.run_simulator()
    cacheSim.display_results()


if __name__ == "__main__": main()
