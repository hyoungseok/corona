import time
import openpyxl
from PyPDF2 import PdfFileMerger

solution = {
    "11-1": "1",
    "11-2": "3",
    "11-3": "-1",
    "11-4": "delta",
    "11-5": "42",
}

pdf_list = [
    "data/test001.pdf",
    "data/test002.pdf",
    "data/test003.pdf",
    "data/test004.pdf",
    "data/test005.pdf",
]

test = ["1", "2", "0", "delta", "41"]

merger = PdfFileMerger()

for pdf in pdf_list:
    merger.append(pdf)

timestamp = time.strftime("%Y%m%d-%H%M%S", time.localtime(time.time()))
merge_name = f"{timestamp}-000.pdf"
merger.write(f"output/{merge_name}")
merger.close()
print(f"pdf exported: {merge_name}")
