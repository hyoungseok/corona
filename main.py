import openpyxl
import collections
import time
from PyPDF2 import PdfFileMerger

solution_file = openpyxl.load_workbook("data/solution.xlsx", data_only=True)
test_file = openpyxl.load_workbook("data/test.xlsx", data_only=True)

solution_sheet = solution_file["solution"]
test_sheet = test_file["test"]

solution = {}
for row in solution_sheet.iter_rows(min_row=2):
    solution[row[0].value] = (row[1].value, row[2].value)

test = collections.defaultdict(list)
for row in test_sheet.iter_rows(min_row=2):
    test[row[0].value].append([row[1].value, row[2].value])

for uid in test:
    merger = PdfFileMerger()
    for qid, answer in test[uid]:
        if solution[qid][0] != answer:
            merger.append(solution[qid][1])

    timestamp = time.strftime("%Y%m%d-%H%M%S", time.localtime(time.time()))
    merge_name = f"{timestamp}-{uid}.pdf"
    merger.write(f"output/{merge_name}")
    merger.close()
    print(f"pdf exported: {merge_name}")
