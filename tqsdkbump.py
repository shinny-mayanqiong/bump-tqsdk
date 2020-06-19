#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
自动完成版本号更新，并且将上一次 tag 到 HEAD 的 commit message 填写到 changelog，还需要手动修改 changelog
用法： python3.7 ./.vscode/bump/bump-version.py --tag=x.x.x
"""
import argparse
import os
from datetime import datetime


def bash_shell(bash_command):
    """
    python 中执行 bash 命令
    :param bash_command:
    :return: bash 命令执行后的控制台输出
    """
    try:
        return os.popen(bash_command).read().strip()
    except:
        return None


def change_version(filename, old_ver, new_ver):
    data = ""
    with open(filename, 'r') as file:
        for line in file:
            if line.find(old_ver) > -1:
                line = line.replace(old_ver, new_ver)
            data += line
    with open(filename, 'w') as file:
        file.write(data)


def change_copyright(filename):
    data = ""
    copyright = f"copyright = u'2018-{datetime.now().strftime('%Y')}, TianQin'\n"
    with open(filename, 'r') as file:
        for line in file:
            if line.find("copyright") == 0:
                line = copyright
            data += line
    with open(filename, 'w') as file:
        file.write(data)


def main():
    if not os.path.isdir(os.path.abspath('./tqsdk/')):
            raise Exception("需要在 tqsdk-python 目录下运行")
    current_branch = bash_shell('git branch --show-current')
    print("current branch:", current_branch)
    if current_branch != "master":
        bash_shell('git checkout master')
        current_branch = bash_shell('git branch --show-current')
        print("current branch:", current_branch)
    old_info = bash_shell('git describe --always --first-parent --tags')
    old_tag = old_info.split('-')[0]
    print("current tag:", old_tag)

    parser = argparse.ArgumentParser()
    parser.add_argument('--tag', type=str, required=True)
    args, unknown = parser.parse_known_args()
    new_tag = args.tag

    if old_tag != new_tag:
        print("start bump version ...........")
        print(f"修改版本号: {old_tag} => {new_tag}")
        # 修改文件中的版本号
        change_version('./tqsdk/__version__.py', old_tag, new_tag)
        change_version('./setup.py', old_tag, new_tag)
        change_version('./doc/conf.py', old_tag, new_tag)
        change_copyright('./doc/conf.py')
        bash_shell('git add ./tqsdk/__version__.py ./setup.py ./doc/conf.py')

        # ./doc/version.rst  添加 changelog， 默认写所有 commit log
        commit = bash_shell('git rev-parse --verify  HEAD')
        print("current commit:", commit)
        logs = bash_shell(f"git log --oneline {old_tag}..{commit}").split('\n')
        data = ""
        with open('./doc/version.rst', 'r') as file:
            for line in file:
                if line.startswith(old_tag):
                    data += f"{new_tag} ({datetime.now().strftime('%Y/%m/%d')})\n\n"
                    for log in logs:
                        start_pos = log.find(' ')
                        data += f"*{log[start_pos:]}\n"
                    data += "\n\n"
                data += line
        with open('./doc/version.rst', 'w') as file:
            file.write(data)
        logs = bash_shell('git add ./doc/version.rst')

    print("接下来需要修改 './doc/version.rst' 里 changelog。然后运行：")
    cmds = ['git add ./doc/version.rst ./tqsdk/__version__.py ./setup.py ./doc/conf.py',
            f"git commit -m 'bump version {new_tag}'",
            f"git push",
            "检查测试用例是否都通过，如果是添加 tag 并提交：",
            f"git tag -a {new_tag} -m \"bump version {new_tag}\" master",
            f"git push --tags"]
    for cmd in cmds:
        print(f"$ {cmd}")


if __name__ == '__main__':
    main()
