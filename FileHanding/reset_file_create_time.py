import subprocess
import pathlib

target_time_human = "08/01/2025 12:00:00"  # 给 SetFile 用
target_time_touch = "202508011200"         # 给 touch 用 (YYYYMMDDhhmm)

base_path = pathlib.Path("/Users/lyu/Code/GitHub/PythonScripts/docx_out")

for file in base_path.glob("**/*"):
    if file.is_file():
        # 改创建时间
        subprocess.run(["SetFile", "-d", target_time_human, str(file)])
        # 改修改时间
        subprocess.run(["SetFile", "-m", target_time_human, str(file)])
        # 如果想同时改访问时间，可用 touch
        subprocess.run(["touch", "-t", target_time_touch, str(file)])