import os
import re


cmd = "python ./SendMail.py"
tmp = os.popen(cmd).read()
print(tmp)

# 输出执行结果
regex = re.compile('summary = .*?\(0.00%\)', re.S)
result = re.findall(regex, tmp)
if len(result) > 0:
    print("successed")
    exit(0)
else:
    print("failed")
    exit(1)
