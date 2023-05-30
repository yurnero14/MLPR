import sys


class BusRecord:
    def __init__(self, busId, lineId, x, y, t):
        self.busId = busId
        self.lineId = lineId
        self.x = x
        self.y = y
        self.t = t
        # we define a class so we can store the data from the file in the object of our class

def loadAllRecords(fName):
    try:
        lRecords = []
        with open(fName) as f:
            for line in f:
                busId, lineId, x, y, t = line.split()
                record = BusRecord(busId, lineId, int(x), int(y), int(t))
                lRecords.append(record)
        return lRecords
        # defining a function here to load the data from file in a list like ex 1 this time we are using a whole
        # separate method for this
    except:
        raise  # If we do not provide an exception, the current exception is propagated


def euclidean_distance(r1, r2):
    return ((r1.x - r2.x) ** 2 + (r1.y - r2.y) ** 2) ** 0.5
    # to basically calculate the distance

def computeBusDistanceTime(lRecords, busId):
    busRecords = sorted([i for i in lRecords if i.busId == busId], key=lambda x: x.t)
    # sorting by using the time because then we have starting time in the start and ending in the end also
    # we have an if condition we will only store busrecords of the iD that is passed as a parameter to this fucntion
    if len(busRecords) == 0:
        return None, None
    totDist = 0.0
    for prev_record, curr_record in zip(busRecords[:-1], busRecords[1:]):
        # [:-1] creates a list without the last item of original list, and [1:] creates a new list but without firstitem
        # zip returns an iterable. it creates a tuples of values from a set of lists and in that order
        # like the first items of each list will be in the first tuple created by zip seperated by comma idk
        # so now we have subsequent euclidean distance between each entry and we add it
        totDist += euclidean_distance(curr_record, prev_record)
    totTime = busRecords[-1].t - busRecords[0].t
    return totDist, totTime
# we are taking care of the first requirement in the above method. also we return total time so we reuse this
# function in average speed calc

def computeLineAvgSpeed(lRecords, lineId):
    lRecordsFiltered = [i for i in lRecords if i.lineId == lineId]
    busSet = set([i.busId for i in lRecordsFiltered])
    # basically to avoid any duplicate entry and to ids to iterate and pass them as params to calc. distance of each
    # bus using the method defined previouslty 
    if len(busSet) == 0:
        return 0.0
    totDist = 0.0
    totTime = 0.0
    for busId in busSet:
        d, t = computeBusDistanceTime(lRecordsFiltered, busId)
        totDist += d
        totTime += t
    return totDist / totTime


if __name__ == '__main__':

    lRecords = loadAllRecords(sys.argv[1])
    if sys.argv[2] == '-b':
        print('%s - Total Distance:' % sys.argv[3], computeBusDistanceTime(lRecords, sys.argv[3])[0])
    elif sys.argv[2] == '-l':
        print('%s - Avg Speed:' % sys.argv[3], computeLineAvgSpeed(lRecords, sys.argv[3]))
    else:
        raise KeyError()
