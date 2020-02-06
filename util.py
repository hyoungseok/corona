import os
import shutil
import json
import openpyxl
import PyPDF2
import time


def list_output(token, course_id):
    return os.listdir(f"output/{token}/course_{course_id}")


def valid_course_id(course_id):
    return f"course_{course_id}" in os.listdir("data")


def read_excel(token, course_id):
    test_file = openpyxl.load_workbook(f"input/{token}/course_{course_id}/test.xlsx", data_only=True)
    test_sheet = test_file["test"]
    row_count = test_sheet.max_row - 1
    if row_count > 5000:
        raise RuntimeError(f"row count limit exceed: {row_count} (> 5000)")
    return test_sheet, row_count


def export_pdf(token, course_id):

    output_path = f"output/{token}/course_{course_id}"
    if os.path.exists(output_path):
        shutil.rmtree(output_path)
    os.makedirs(output_path)

    solution = json.load(open(f"data/course_{course_id}/solution.json", "r"))
    test_sheet, _ = read_excel(token, course_id)

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
            merger.write(f"{output_path}/{merge_name}")
            merger.close()
            print(f"pdf exported: {merge_name}")
        else:
            print(f"all clear: {tid}-{name_map[uid]}")

    print("evaluation finished")
