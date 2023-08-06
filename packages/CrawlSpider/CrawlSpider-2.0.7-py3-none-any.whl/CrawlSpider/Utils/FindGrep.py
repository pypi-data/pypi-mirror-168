# -*- coding: utf-8 -*-
# __author__ : Ricky
# __createTime__ : 2022/9/22 1:01
# __fileName__ : CrawlSpider FindGrep.py
# __devIDE__ : PyCharm

import fire
import sys
import re
from loguru import logger

# logger.add(sys.stdout, colorize=True, format="<green>{time}</green> <level>{message}</level>")

fieldDic = {
    'psg': {
        'fieldList': 'UID          PID    PPID  C STIME TTY          TIME CMD'.split(),
        'isRmSpace': True
    }
}


def judgeMentCondition(line: str, grep: str, reg=None, isReg=False):
    b = False
    if not isReg:

        if all(['(' in grep, '(' in grep]):
            sList = []
            rightIndexs = []

            startIndex = 0
            while ')' in grep[startIndex:]:
                index = grep.index(')', startIndex)
                rightIndexs.append(index)
                leftIndex = grep.index('(', startIndex, index)
                sList.append(grep[leftIndex: index + 1])
                startIndex = index + 1

            for s in sList:
                _grep = s[1:-1]
                b = False
                if '||' in _grep:
                    b = any([cond in line for cond in _grep.split('||')])
                elif '&&' in _grep:
                    b = all([cond in line for cond in _grep.split('&&')])
                if b:
                    repl = grep[:5]
                else:
                    repl = ','.join(['None' for i in range(5)])
                grep = grep.replace(s, repl)
            # print(f"grep: {grep}--sList: {sList}")

        if '||' in grep:
            b = any([cond in line for cond in grep.split('||')])
        elif '&&' in grep:
            b = all([cond in line for cond in grep.split('&&')])
        else:
            b = grep in line

    else:
        b = re.findall(reg, line)

    return b


def find(filePath, grep=None, head=5, tail=5, isReg=False, delimiter='\n', bSize=None, seek=0, whence=0, isLog=True,
         startLine=0, endLine=0):
    """analysis file to locate the lines by feature

    Args:
        filePath (_type_): file for operate.
        grep (_type_, optional):feature,eg: error.
        head (int, optional): file head lines.
        tail (int, optional): file tail lines.
        isReg (bool, optional): grep is or not regex expression.
        delimiter (str, optional): split file for lines by delimiter.
        bSize (_type_, optional): how much size to read file.
        seek (int, optional): file cursor position.
        whence (int, optional): 0 means from the file header, 1 means relative current position, 2 means from file tailer.
    """

    with open(filePath, 'r', encoding='utf-8') as fr:
        fr.seek(seek, whence)
        lines = [line for line in fr.read(bSize).split(delimiter)]
        Len = len(lines)
        if isLog:
            logger.info(f"--- totalLine: {Len} ---")
        startLine = startLine if startLine < Len else 0
        endLine = Len if endLine >= Len else Len if endLine == 0 else endLine
        lineDic = {
            str(i + 1): lines[i]
            for i in range(startLine, endLine)
        }
        if not grep:
            if isLog:
                logger.info(f"---context---")
            headLines = '\n'.join([
                f"No{i + 1}\t{lineDic[str(i + 1)]}"
                for i in range(head) if startLine < i + 1 <= endLine
            ])
            print(headLines)
            if isLog:
                logger.info(f"--- sep ---")

            tailLines = '\n'.join([
                f"No{Len - tail + i + 1}\t{lineDic[str(Len - tail + i + 1)]}"
                for i in range(tail) if startLine < Len - tail + i + 1 <= endLine
            ])
            print(tailLines)
        else:
            grep = str(grep)
            regExp = None
            if isReg:
                regExp = re.compile(grep)
            indexs = [k for k in lineDic if judgeMentCondition(lineDic[k], grep, regExp, isReg=isReg)]
            for index in indexs:
                if isLog:
                    logger.info(f"---context-{index}---")
                headLines = '\n'.join([
                    f"No{int(index) - head + i}\t{lineDic[str(int(index) - head + i)]}"
                    for i in range(head) if startLine < int(index) - head + i <= endLine
                ])
                print(headLines)
                if isLog:
                    logger.error(f"find: No{index}\t{lineDic[index]}")
                    logger.info(f"--- sep-{index}  ---")
                else:
                    print(f"find: No{index}\t{lineDic[index]}")
                tailLines = '\n'.join([
                    f"No{int(index) + 1 + i}\t{lineDic[str(int(index) + 1 + i)]}"
                    for i in range(tail) if startLine < int(index) + 1 + i <= endLine
                ])
                print(tailLines)


def stream(delimiter='', index='all', field=None, command=None, toLog=False, isRmSpace=True):
    """对 shell stdin/stdout 流进行操作

    Args:
        delimiter (str, optional): _description_. Defaults to '\t'.
        colIndex (int, optional): _description_. Defaults to 0.
    """
    hasHeader = False
    for line in sys.stdin:
        line = line.strip()
        if line:
            tmpList = line.split(delimiter) if delimiter else line.split()
            streamHandler(tmpList, index, field, command, toLog=toLog, hasHeader=hasHeader, isRmSpace=isRmSpace)
            hasHeader = True


def streamHandler(tmpList, index, field, command, toLog=False, hasHeader=True, isRmSpace=False):
    if isinstance(index, (tuple, list)):
        index = ','.join([str(i) for i in index])
    indexs = [int(v) for v in str(index).split(',') if v.strip()] if 'all' not in index else []
    fields = [v.strip().upper() for v in str(field).split(',') if v.strip()]

    if isRmSpace:
        tmpList = [v for v in tmpList if v.strip()]

    if command and command in fieldDic:
        dic = fieldDic[command]
        fieldList = dic['fieldList']

        if fields:
            inds = [fieldList.index(field) for field in fields if field in fieldList]
            if inds:
                indexs = inds

        l = tmpList[:len(fieldList) - 1]
        l.append(' '.join(tmpList[len(fieldList) - 1:]))
        tmpList = l
        if not hasHeader:
            print(f"hasHeader: {hasHeader}")
            headers = '\t'.join([fieldList[index] for index in indexs] if indexs else fieldList)
            if toLog:
                logger.info(headers)
            else:
                print(headers)
    info = '\t'.join([tmpList[index] for index in indexs] if indexs else tmpList)
    if toLog:
        logger.info(info)
    else:
        print(info)


if __name__ == '__main__':
    fire.Fire({
        'find': find,
        'head': lambda *args, **kwargs: find(*args, tail=0, **kwargs),
        'tail': lambda *args, **kwargs: find(*args, head=0, **kwargs),
        'stream': stream
    })

