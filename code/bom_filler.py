import csv
import numpy as np
import sys

npStrDtype = '<U42'

def read_csv(filename, delimeter = ",", skip_header = 0):
    csv_handler = csv.reader(open(filename, newline='\n'), delimiter=delimeter)
    csv_handler = zip(*list(csv_handler)[skip_header:])
    content = list()

    for n, line in enumerate(csv_handler):
        content.append(list())
        for item in line:
            content[-1].append(item)

    return np.transpose(np.array(content))

print(sys.argv)

stkSum = read_csv(sys.argv[1])


item_list = stkSum[:, 0]


newStkSum = np.ndarray(shape = (len(stkSum), len(sys.argv) - 1),
					   dtype = npStrDtype)
newStkSum[:, 0] = item_list


for bom_idx, bom_name in enumerate(sys.argv[2:-1]):
	print(bom_idx, bom_name)
	bom = read_csv(bom_name, skip_header = 8)
	for idx, item in enumerate(bom[:-7, 0]):
		if item:
			srch_idx = np.where(item_list == item)
			newStkSum[srch_idx, 1 + bom_idx] = bom[idx + 1, 1]


np.savetxt(sys.argv[-1], newStkSum, delimiter="!", fmt = '%s')
