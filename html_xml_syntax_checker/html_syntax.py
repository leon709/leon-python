import re

import string


def load_test_cases():
    """
    这个方法就是读取加载 Test Cases，默认文件是 text_cases.txt
    每个 test case 是一段文本，且可能有多行，我们用一个字符串列表来保存一个 test case
    :return:
    """
    with open('./test_cases.txt') as f:
        cases = []
        case = []
        nl = None
        for l in f:
            if l.strip() == '0':
                break
            if nl is None and re.match(r'\d+', l.strip()):
                nl = int(l.strip())
                continue
            if nl and len(case) < nl:
                case.append(l)
                if len(case) == nl:
                    cases.append(case)
                    case = []
                    nl = None
    return cases


def syntax_check(case):
    """
    HTML 检查核心逻辑

    对一个 test case 是个多行的字符串列表，且tag 是的开始和结束是可以跨行，也可以嵌套，但不能交叉
     * 遍历每行字符串，用正则查找 tag ，但是正则不匹配标签的末尾字符`>` （留着检查）
     * 一行没有匹配到标签，跳过本行
     * 匹配到标签的行，开始校验标签：
      1。 先取匹配到的标签的下一个字符，如果不是'>' ，那说明这个标签不正确，有可能是长度过长或者是没有 `>` 结束

      2。 如果匹配到了正确的tag，先看这个tag 是个 `结束tag` 还是个 `开头tag`。
          对结束tag：则要检查前面有没有开头tag，每个tag 我们放入 tag stack，所以是查看栈顶，匹配成功则 pop
          对开头tag：栈顶押入一个期望的对结束tag

     * 所有行处理完，检查 tag stack 里是否还有元素，有的话说明存在没有结束的tag，报错
    :param case:
    :return:
    """
    tag_stack = []
    for _, line in enumerate(case):
        ln = _ + 1
        matches = re.findall(r'</?[a-zA-Z]{0,10}', line)
        if not matches:
            # no tag found
            continue

        for tg in matches:
            next_char = line[line.find(tg) + len(tg)]
            if next_char != '>':
                if next_char in string.ascii_letters:
                    return f'line {ln}: too many/few characters in tag name'
                return f'line {ln}: bad character in tag name'
            if len(tg) <= 2:
                return f'line {ln}: too many/few characters in tag name'

            if tg[1] == '/':
                # so it is an end tag, let's verify
                expected = tag_stack[-1] if tag_stack else None
                if not expected:
                    return f'line {ln}: no matching begin tag'
                elif (tg + '>') != expected:
                    return f'line {ln}: expected {expected}'
                else:
                    tag_stack.pop()
            else:
                # it is an start tag, expect an end tag, add to tag stack
                expected = '</' + tg[1:] + '>'
                tag_stack.append(expected)
    if tag_stack:
        # at last, if there is tag in tag stack, means some tags not ended.
        expected = tag_stack[-1]
        return f'line {ln}: expected {expected}'


if __name__ == '__main__':
    all_cases = load_test_cases()

    for i, c in enumerate(all_cases):
        # for l in c:
        #     print(l, end='')
        # print('-' * 100)
        rs = syntax_check(c)
        if not rs:
            rs = 'OK'
        print(f'Test Case {i + 1}')
        print(rs)
        print('-' * 100)
