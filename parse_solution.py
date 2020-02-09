import os
import re
import json

solution_name_pattern = re.compile("^[0-9]{6}\\.pdf$")


def convert_file_name(course_id):
    course_path = f"data/course_{course_id}"
    file_name_list = os.listdir(course_path)
    for file_name in file_name_list:
        if (not solution_name_pattern.match(file_name)) and (file_name != f"solution_{course_id}.tsv"):
            split_file_name = file_name.replace(".pdf", "").split("_")
            test_id = int(split_file_name[1].replace("part", ""))
            question_id = int(split_file_name[2].replace("part", ""))
            solution_id = f"{course_id:02d}{test_id:02d}{question_id:02d}"
            os.rename(f"{course_path}/{file_name}", f"{course_path}/{solution_id}.pdf")

    print("convert finished")


def update_solution(course_id):
    if os.path.exists("data/solution.json"):
        solution = json.load(open("data/solution.json"))
    else:
        solution = {}

    course_path = f"data/course_{course_id}"
    with open(f"{course_path}/solution_{course_id}.tsv", "r") as solution_tsv:
        read_solution = solution_tsv.readlines()
        for test_id, line in enumerate(read_solution):
            split_line = line.strip().split("\t")
            for question_id, answer in enumerate(split_line):
                solution_id = f"{course_id:02d}{test_id + 1:02d}{question_id + 1:02d}"
                pdf_path = f"{course_path}/{solution_id}.pdf"
                solution[solution_id] = {"answer": int(answer), "pdf": pdf_path}
        json.dump(solution, open(f"data/solution.json", "w"), indent=2)

    print("solution update finished")


if __name__ == "__main__":
    course_id = 11
    convert_file_name(course_id)
    update_solution(course_id)
