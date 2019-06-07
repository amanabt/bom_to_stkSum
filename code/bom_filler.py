# Usage 1 :  python bom_filler.py StkSum.csv BOM.csv newStkSum.csv
# Usage 2 :  python bom_filler.py StkSum.csv BOM1.csv BOM2.csv newStkSum.csv

import csv
import numpy as np
import sys

HEADER_SIZE = 1
npStrDtype = '<U42'

def read_csv(filename, delimeter = ",", skip_header = 0):
    csv_handler = csv.reader(open(filename), delimiter=delimeter)
    csv_handler = zip(*list(csv_handler)[skip_header:])
    content = list()

    for n, line in enumerate(csv_handler):
        content.append(list())
        for item in line:
            content[-1].append(item)

    return np.transpose(np.array(content))

def display_filepaths():

	print ("\n")
	print "######################################################"
	print "Stock Summary \t\t :  ", sys.argv[1]
	for bom_index, bom_name in enumerate(sys.argv[2:-1]):
		print "BOM", bom_index, " \t\t\t : ", bom_name
	print "Stock Flow Summary \t : ", sys.argv[-1]
	print "######################################################"
	print ("\n")


display_filepaths()

stkSum = read_csv(sys.argv[1])
item_list = stkSum[:, 0]


newStkSum = np.ndarray(shape = (len(stkSum)+1, len(sys.argv) - 1),
					   dtype = npStrDtype)

# Reserve rows for headers
newStkSum[0, 0] = "Stock Item"

# Populate stock items
newStkSum[1:, 0] = item_list

# Enter stock quantities used by each BOMs
for bom_index, bom_name in enumerate(sys.argv[2:-1]):

	# Populate column heading
	newStkSum[0, 1 + bom_index] = bom_name

	bom = read_csv(bom_name, skip_header = 8)
	for index, item in enumerate(bom[:-7, 0]):
		if item:
			search_index = np.where(item_list == item)
			newStkSum[search_index[0][0]+1, 1 + bom_index] = bom[index + 1, 1]

# Exported file opens with field delimiter set to '!'
np.savetxt(sys.argv[-1], newStkSum, delimiter="!", fmt = '%s')