# git_push.py
import os
import datetime
import subprocess
from pathlib import Path

# 仓库路径（修改为您的实际路径）
REPO_PATH = r"C:/Users/Administrator/Documents/note/协议"  

def run_command(command):
    """执行命令并返回结果"""
    try:
        process = subprocess.run(
            command,
            cwd=REPO_PATH,
            check=True,
            text=True,
            shell=True,
            capture_output=True
        )
        return True, process.stdout
    except subprocess.CalledProcessError as e:
        return False, f"Error: {e.stderr}"

def git_push():
    """执行 Git 推送操作"""
    # 获取当前时间
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Git 操作序列
    commands = [
        "git status",
        "git add .",
        f'git commit -m "Auto commit: {now}"',
        "git push origin main"
    ]
    
    print(f"开始推送... 当前时间: {now}")
    print(f"仓库路径: {REPO_PATH}")
    
    # 执行每个命令
    for cmd in commands:
        print(f"\n执行: {cmd}")
        success, output = run_command(cmd)
        print(output)
        
        if not success:
            print(f"命令执行失败: {cmd}")
            return False
    
    return True

if __name__ == "__main__":
    # 检查路径是否存在
    if not Path(REPO_PATH).exists():
        print(f"错误：路径不存在 - {REPO_PATH}")
        exit(1)
    
    # 执行推送
    if git_push():
        print("\n成功推送到仓库！")
    else:
        print("\n推送失败，请检查错误信息")
    
    # 等待用户输入后退出
    input("\n按 Enter 键退出...")