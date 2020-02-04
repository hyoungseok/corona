import json
import openpyxl
import PyPDF2
import time

solution = json.load(open("data/solution.json", "r"))

test_file = openpyxl.load_workbook("input/test.xlsx", data_only=True)
test_sheet = test_file["test"]

name_map = {}
test_result = []
for row in test_sheet.iter_rows(min_row=2):
    name = row[0].value
    uid = row[1].value
    tid = row[2].value
    answer = [[f"{tid}{i + 1:02d}", row[i + 3].value] for i in range(25)]
    name_map[uid] = name
    test_result.append([uid, answer])

for uid, test in test_result:
    merger = PyPDF2.PdfFileMerger()
    tid = test[0][0][:4]
    wrong_answer_count = 0
    for qid, answer in test:
        if solution[qid]["answer"] != answer:
            wrong_answer_count += 1
            merger.append(solution[qid]["pdf"])

    if wrong_answer_count > 0:
        timestamp = time.strftime("%Y%m%d-%H%M%S", time.localtime(time.time()))
        merge_name = f"{timestamp}-{tid}-{name_map[uid]}.pdf"
        merger.write(f"output/{merge_name}")
        merger.close()
        print(f"pdf exported: {merge_name}")
    else:
        print(f"all clear: {tid}-{name_map[uid]}")

print("evaluation finished")
