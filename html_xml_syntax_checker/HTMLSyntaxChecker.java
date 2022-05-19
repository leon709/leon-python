import java.io.*;
import java.util.ArrayList;
import java.util.List;
import java.util.Stack;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

class SyntaxChecker {
    private List<String> input;
    Pattern TAGPATTERN = Pattern.compile("</?[a-z]{0,10}", Pattern.CASE_INSENSITIVE);

    SyntaxChecker(List<String> input) {
        this.input = input;
    }

    /**
     * 查找本行里有没有标签出现
     * @param line
     * @return
     */
    public List<String> findAll(String line) {
        Matcher m = TAGPATTERN.matcher(line);
        List<String> found = new ArrayList<>();
        while (m.find()) {
            found.add(m.group());
        }
        return found;
    }

    /**
     * 核心代码
     * 对一个 test case 是个多行的字符串列表，且tag 是的开始和结束是可以跨行，也可以嵌套，但不能交叉
     * 遍历每行字符串，用正则查找 tag ，但是正则不匹配标签的末尾字符`>` （留着检查）
     * 一行没有匹配到标签，跳过本行
     * 匹配到标签的行，开始校验标签：
     * 1。 先取匹配到的标签的下一个字符，如果不是'>' ，那说明这个标签不正确，有可能是长度过长或者是没有 `>` 结束
     * 2。 如果匹配到了正确的tag，先看这个tag 是个 `结束tag` 还是个 `开头tag`。
     *     对结束tag：则要检查前面有没有开头tag，每个tag 我们放入 tag stack，所以是查看栈顶，匹配成功则 pop
     *     对开头tag：栈顶押入一个期望的对结束tag
     * 3。 所有行处理完，检查 tag stack 里是否还有元素，有的话说明存在没有结束的tag，报错
     * @return
     */
    public String check() {
        Stack<String> tagStack = new Stack();
        int ln = 0;
        for(int i=0; i< this.input.size(); i++) {
            String line = this.input.get(i);
            ln = i + 1;
            List<String> matches = findAll(line);
            if (matches == null || matches.isEmpty()) {
                // no tag found
                continue;
            }
            for(String tg: matches) {
                // verify next char to make sure it is valid tag, because regex did not matched `>`
                int nextCharAt = line.indexOf(tg) + tg.length();
                char nextChar = nextCharAt < line.length() ? line.charAt(nextCharAt) : '\n';
                if (nextChar != '>') {
                    // so this tag is not valid
                    int v = nextChar;
                    if ((v >= 65 && v <= 90 ) || (v >= 97 && v <= 122)){
                        return String.format("line %d : too many/few characters in tag name", ln);
                    }
                    return String.format("line %d : bad character in tag name", ln);
                }
                if (tg.length() <= 2) {
                    return String.format("line %d : too many/few characters in tag name", ln);
                }
                if (tg.charAt(1) == '/') {
                    // so it is an end tag, let's verify
                    String expected = tagStack.size() > 0 ? tagStack.get(tagStack.size() - 1) : null;
                    if (expected == null) {
                        return String.format("line %d : no matching begin tag", ln);
                    } else if (!expected.replace(tg, "").equals(">")) {
                        return String.format("line %d : expected %s", ln, expected);
                    } else {
                        // matched the start tag and pop
                        tagStack.pop();
                    }
                } else {
                    // it is an start tag, expect an end tag, add to tag stack
                    tagStack.push("</".concat(tg.substring(1)).concat(">"));
                }
            }
        }
        if (tagStack.size() > 0) {
            // at last, if there is tag in tag stack, means some tags not ended.
            String expected = tagStack.get(tagStack.size() - 1);
            return String.format("line %d : expected %s", ln, expected);
        }
        return "OK";
    }
}

public class HTMLSyntaxChecker {
    static Pattern NL = Pattern.compile("^\\d+$");
//    public static List<String[]> cases = new ArrayList<>();

    /**
     * 这个方法就是读取加载 Test Cases，默认文件是 text_cases.txt
     * 每个 test case 是一段文本，且可能有多行，我们用一个字符串列表来保存一个 test case
     * @param filePath
     * @return
     * @throws IOException
     */
    public static List<List<String>> loadTestCases(String filePath) throws IOException {
        List<List<String>> cases = new ArrayList<>();
        InputStream is = new FileInputStream(filePath);
        try {
            BufferedReader br = new BufferedReader(new InputStreamReader(is));
            String line;
            int nl = 0;
            List<String> oneCase = new ArrayList<>();
            while ((line=br.readLine()) != null) {
                if (line.trim().equals("0")) {
                    break;
                }
                if (nl == 0 && NL.matcher(line).find()) {
                    nl = Integer.parseInt(line.trim());
                    continue;
                }
                if (nl > 0 && oneCase.size() < nl) {
                    oneCase.add(line);
                    if (oneCase.size() == nl) {
                        cases.add(oneCase);
                        oneCase = new ArrayList<>();
                        nl = 0;
                    }
                }
            }
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            if (is != null) {
                is.close();
            }
        }
        return cases;
    }

    public static void main(String[] args) throws IOException {
        // testcases 文件路径
        String testCasesFile = "./test_cases.txt";
        List<List<String>> testCases = loadTestCases(testCasesFile);
        for (int i = 0; i < testCases.size(); i++) {
            List<String> testCase = testCases.get(i);
            String result = new SyntaxChecker(testCase).check();
            System.out.println("Test Case ".concat(String.valueOf(i + 1)));
            System.out.println(result);
            System.out.println("----------------------");
        }
    }
}
