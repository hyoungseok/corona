import json

course_id = 11
course_solution_prefix = "구선문 오답노트 수학(상)"

solution = {}
with open("data/solution.tsv", "r") as solution_tsv, open("data/solution.json", "w") as solution_json:
    read_solution = solution_tsv.readlines()
    for test_id, line in enumerate(read_solution):
        split_line = line.strip().split("\t")
        for question_id, answer in enumerate(split_line):
            qid = f"{course_id:02d}{test_id + 1:02d}{question_id + 1:02d}"
            pdf = f"data/solution/{course_solution_prefix}_part{test_id + 1}_part{question_id + 1}.pdf"
            solution[qid] = {"answer": int(answer), "pdf": pdf}
    json.dump(solution, solution_json)

print("solution json done")
