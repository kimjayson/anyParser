# -*- coding: utf-8 -*-

jsonStr = '{"a":1,"b":true,"c":false,"foo":null,"bar":[1,2,3]}'
i = 0

# 先定义大的框架
def parseValue(string):
    if string[i] == '{':
        return parseObject(string)
    elif string[i] == '[':
        return parseArray(string)
    elif string[i] == 'n':
        return parseNull(string)
    elif string[i] == 't':
        return parseTrue(string)
    elif string[i] == 'f':
        return parseFalse(string)
    elif string[i] == '"':
        return parseString(string)
    else:
        return parseNumber(string)

# 之后一步步实现每个函数
# 所有的函数都是从i位置开始解析出一个对应类型的值，同时把i移动到解析完成后的下一位
def parseString(string):
    res = ''
    global i
    i += 1 # 开始解析之前，i是指向字符开始的双引号，但字符不能包括双引号
    while string[i] != '"':
        res += string[i]
        i += 1
    i += 1 # 解析完移动到下一个位置
    return res

def parseNull(string): # 简单粗暴，直接往后读4个字符出来
    global i

    content = string[i:i+4]
    if content == 'null':
        i += 4
        return None
    else:
        raise Exception('Unexpected char at pos: {}'.format(i))

def parseFalse(string):
    global i

    content = string[i:i+5]
    if content == 'false':
        i += 5
        return False
    else:
        raise Exception('Unexpected char at pos: {}'.format(i))

def parseTrue(string):
    global i
    content = string[i:i+4]
    if content == 'true':
        i += 4
        return True
    else:
        raise Exception('Unexpected char at pos: {}'.format(i))

def parseNumber(string):
    global i
    '''
    // 本函数的实现并没有考虑内容格式的问题，实际上JSON中的数值需要满足一个格式
    // 不过好在这个格式基本可以用正则表达出来，不过这里就不写了
    // 想写的话对着官网的铁路图写一个出来就行了
    // 并且由于最后调用了parseFloat，所以如果格式不对，还是会报错的
    '''
    numStr = '' # -2e+8 此处只要判断i位置还是数字字符，就继续读 ;为了方便，写了另一个helper函数
    while isNumberChar(string[i]):
        numStr += string[i]
        i += 1
    return numStr

# 判断字母C是否是组成数值的符号
def isNumberChar(c):
    chars = {'-':True,'+':True,'e':True,'E':True,'.':True}
    if chars.get(c):
        return True
    if c >= '0' and c <= '9':
        return True
    return False

# 解析数组,掐头去尾，一个值一个逗号，如果解析完一个值没有逗号，说明完成了
def parseArray(string):
    global i

    i += 1
    result = [] # [123,"asdf",true,false]
    while string[i] != ']':
        result.append(parseValue(string))
        if string[i] == ',':
            i += 1
    i += 1
    return result

# 解析对象，一如既往，掐头去尾，一个值可能是任意类型，调用parseValue，逗号下一组，没有解析完毕
def parseObject(string):
    global i

    i += 1
    result = {} # {"a":1,"b":"c"}
    while string[i] != '}':
        key = parseString(string)
        i += 1 # 直接跳过冒号：
        value = parseValue(string)
        result[key] = value
        if string[i] == ',':
            i += 1
    i += 1
    return result

# 整个内容其实表示一个值，所以要把i置为0，然后从头解析出来一个值就可以
def parse(jsonStr):
    string = jsonStr
    return parseValue(string)


if __name__ == '__main__':
    res = parse(jsonStr)
    print(res)

"""
todo：
1.封装类
2.处理空白，支持转义字符，unnicode转义符\u6211
3.做json序列器
4.做json格式化输出器
"""

