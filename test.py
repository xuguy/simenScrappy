'''
basically trash file, only for testing if dataProcess.py imported as expected
'''
import dataProcess

dataNames = dataProcess.getDataFileNames()

# count total number of userid
count=0
for names in dataNames:
    start, stop = dataProcess.startStopRec(names)
    count+= (stop-start)+1

missing_id_test = dataProcess.getMissingID(dataNames)

missingPct = missing_id_test.shape[0]/count
print(f'percentage of missing userid: {missingPct*100:.2f}% out of {count} users')
