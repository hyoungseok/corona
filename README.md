# corona
## overview
1. read `test.xlsx` (name, uid, tid, qid, answer)
2. parse `solution.tsv` (qid, answer, pdf path)
3. return `[timestamp]-[tid]-[name].pdf`

## requirement
+ ubuntu==18.04
+ python==3.6
+ PyPDF2==1.26.0
+ openpyxl==3.0.3
+ Flask==1.1.1
