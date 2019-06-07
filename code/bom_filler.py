import csv
import numpy as np

def read_csv(filename, delimeter = ",", skip_header = 0):
    csv_handler = csv.reader(open(filename, newline='\n'), delimiter=delimeter)
    csv_handler = zip(*list(csv_handler)[skip_header:])
    content = list()

    for n, line in enumerate(csv_handler):
        content.append(list())
        for item in line:
            content[-1].append(item)

    return np.transpose(np.array(content))

stkSum = read_csv('../Sample_Data/StkSum.csv')
item_list = stkSum[:, 0]

bom = read_csv('../Sample_Data/NVM.csv', skip_header = 8)
npStrDtype = '<U42'

newStkSum = np.ndarray(shape = (len(stkSum), 2), dtype = npStrDtype)
newStkSum[:, 0] = item_list

for idx, item in enumerate(bom[:-7, 0]):
    if item:
        srch_idx = np.where(item_list == item)[0][0]
        newStkSum[srch_idx, 1] = bom[idx + 1, 1]

np.savetxt("newStkSum.csv", newStkSum, delimiter="!", fmt = '%s')
