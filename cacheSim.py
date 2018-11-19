import math
import argparse
inputFile = 1

class CacheSim:

    blockSizeList = {2, 4, 8, 16, 32, 64}
    waysList = {0, 1, 2, 4, 8, 16}
    vCacheSizeList = {0, 4, 8, 16}

    inputFile = ""      # Input File
    cacheSize = 1      # Cache Size
    blockSize = 2      # Block Size
    ways = 1           # Associativity
    vCacheSize = 0      # VCS

    setsCount = 0
    linesCount = 0
    hits = 0
    misses = 0

    instructions = []
    cache = []
    victimCache = []

    def setupSimulator(self):
        inputFileName, cacheSize, blockSize, ways, vCacheSize = self.inputCacheProperties()
        self.inputFile = "inputFiles/" + inputFileName
        if cacheSize not in range(1, 4097):
            print "Incorrect Input CS %s" % cacheSize
            exit(-1)
        self.cacheSize = cacheSize*1024
        if blockSize not in self.blockSizeList:
            print "Incorrect Input BS"
            exit(-1)
        self.blockSize = blockSize
        if ways not in self.waysList:
            print "Incorrect Input ways"
            exit(-1)
        if ways == 0:
            self.ways = self.cacheSize / self.blockSize
            self.setsCount = 1
        else:
            self.ways = ways
            self.setsCount = self.cacheSize / self.blockSize / ways
        self.linesCount = self.setsCount * ways

        if vCacheSize not in self.vCacheSizeList:
            print "Incorrect Input VCS"
            exit(-1)
        self.vCacheSize = vCacheSize
        self.openInputFile()

    def runSimulator(self):
        self.initializeCache()
        self.initializeVictimCache()
        print("Starting Cache Simulation ...\n")
        for instruction in self.instructions:
            address = int(instruction.split()[2], 16)
            offset = int(instruction.split()[1])
            address = address + offset
            address %= (2 ** 32)
            index = address >> int(math.log(self.blockSize, 2))
            index %= self.setsCount
            tag = address >> int(math.log(self.setsCount, 2) +
                                 math.log(self.blockSize, 2))
            self.findInCache(self.cache, index, tag)
        print "Cache Simulation Complete ...\n"

    def findInCache(self, cache, index, tag):
        for set in range(len(self.cache)):
            if cache[set]["index"] == index:
                for line in range(self.ways):
                    if cache[set]["lines"][line]["tag"] == tag:
                        self.hits += 1
                        usedLine = cache[set]["lines"][line]
                        cache[set]["lines"].pop(line)
                        cache[set]["lines"].insert(0, usedLine)
                        usedSet = cache[set]
                        cache.pop(set)
                        cache.insert(0, usedSet)
                        return
                self.misses += 1
                self.checkVictimCache(self.victimCache, index, tag)
                newLine = self.newCacheLine(tag)
                lru_Line = cache[set]["lines"].pop()
                self.addToVictimCache(index, lru_Line["tag"])
                cache[set]["lines"].insert(0, newLine)
                usedSet = cache[set]
                cache.pop(set)
                cache.insert(0, usedSet)
                return
        self.misses += 1
        self.checkVictimCache(self.victimCache, index, tag)
        newSet = self.newCacheSet(index, tag)
        lru_Set = cache.pop()
        self.addSetToVictimCache(lru_Set)
        cache.insert(0, newSet)
        return

    def newCacheSet(self, index, tag):
        cacheSet = {}
        cacheSet["index"] = index
        cacheSet["lines"] = []
        for line in range(self.ways):
            cacheSet["lines"].insert(line, self.newCacheLine(0))
        cacheSet["lines"][0]["tag"] = tag
        return cacheSet

    def newCacheLine(self, tag):
        line = {}
        line["tag"] = tag
        return line

    def checkVictimCache(self, victimCache, index, tag):
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

    def addToVictimCache(self, index, tag):
        if self.vCacheSize == 0:
            return
        vCacheLine = {}
        vCacheLine["index"] = index
        vCacheLine["tag"] = tag
        self.victimCache.pop()
        self.victimCache.insert(0, vCacheLine)

    def addSetToVictimCache(self, lru_Set):
        line = 0
        while (line < self.vCacheSize) and (line < len(lru_Set["lines"])):
            self.addToVictimCache(lru_Set["index"], lru_Set["lines"][line]["tag"])
            line += 1

    def inputCacheProperties(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("-i", "--i", help="inputFileName", type=str)
        parser.add_argument("-cs", "--cs", help="cacheSize", type=int)
        parser.add_argument("-bs", "--bs", help="blockSize", type=int)
        parser.add_argument("-w", "--w", help="ways", type=int)
        parser.add_argument("-vs", "--vs", help="victimCacheSize", type=int)
        args = parser.parse_args()
        i = args.i
        cs = args.cs
        bs = args.bs
        w = args.w
        vcs = args.vs
        return i, cs, bs, w, vcs

    def openInputFile(self):
        print "\nReading %s ...\n" % self.inputFile
        with open(self.inputFile) as content:
            self.instructions = content.readlines()

    def initializeCache(self):
        if self.ways == (self.cacheSize / self.blockSize):
            mapping = "fully-associative"
        elif self.ways == 1:
            mapping = "direct-mapped"
        else:
            mapping = str(self.ways) + "-way set associative"
        print "Initializing %s Cache of %s KB ...\n" % (mapping,
                                                        (self.cacheSize)/1024)
        for set in range(self.setsCount):
            self.cache.insert(set, self.newCacheSet(0, 0))
        print "**Initialization complete**\n"

    def initializeVictimCache(self):
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

    def addressStructure(self):
        offset_bits = int(math.log(self.blockSize, 2))
        index_bits = int(math.log(self.setsCount, 2))
        tag_bits = 32 - offset_bits - index_bits
        return index_bits, offset_bits, tag_bits

    def showResults(self):
        index_bits, offset_bits, tag_bits = self.addressStructure()
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
    cacheSim.setupSimulator()
    cacheSim.runSimulator()
    cacheSim.showResults()
    
if __name__ == "__main__": main()



