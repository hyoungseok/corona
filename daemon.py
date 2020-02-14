import os
import re
import time
import util

start_pattern = re.compile("^start_[a-zA-Z0-9]+$")

print(f"startDaemon={int(time.time())}")
while os.path.exists(f"state/daemon"):
    time.sleep(5)
    print(f"aliveCheck={int(time.time())}")
    file_list = os.listdir("state")

    start_match = list(filter(start_pattern.match, file_list))
    if start_match:
        print(f"startEval={int(time.time())}")
        token = start_match[0].split("_")[-1]
        os.rename(f"state/start_{token}", f"state/finish_{token}")
        util.export_pdf(token)
        util.zip_all(token)
