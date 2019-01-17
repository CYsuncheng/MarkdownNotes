# LeetCode练习一

## 题目1
在大小为 2N 的数组 A 中有 N+1 个不同的元素，其中有一个元素重复了 N 次。返回重复了 N 次的那个元素。

### 测试用例
[1,2,3,3]
[2,1,2,5,3,2]
[5,1,5,2,5,3,5,4]

### 代码

Python

``` Python
class Solution(object):
    def repeatedNTimes(self, A):
        """
        :type A: List[int]
        :rtype: int
        """
        l = 0
        for i in range(len(A)):
            if A.count(A[i]) == len(A)/2:
                l = A[i]
        return l
```

Java

``` Java
public int repeatedNTimes_1(int[] A) {
    int res = A[0];
    int[] countArr = new int[10000];
    for (int i : A) {
        countArr[i]++;
        if (countArr[i] == A.length / 2) {
            res = i;
            break;
        }
    }
    return res;
}

public int repeatedNTimes(int[] A) {
    Arrays.sort(A);
    return A[A.length / 2] == A[A.length - 1] ? A[A.length - 1] : A[A.length / 2 - 1];
}
```

## 题目2
每封电子邮件都由一个本地名称和一个域名组成，以 @ 符号分隔。
例如，在 alice@leetcode.com中， alice 是本地名称，而 leetcode.com 是域名。
除了小写字母，这些电子邮件还可能包含 ',' 或 '+'。

    1. 如果在电子邮件地址的本地名称部分中的某些字符之间添加句点（'.'），则发往那里的邮件将会转发到本地名称中没有点的同一地址。例如，"alice.z@leetcode.com” 和 “alicez@leetcode.com” 会转发到同一电子邮件地址。（请注意，此规则不适用于域名。）
    2. 如果在本地名称中添加加号（'+'），则会忽略第一个加号后面的所有内容。这允许过滤某些电子邮件，例如 m.y+name@email.com 将转发到 my@email.com。 （同样，此规则不适用于域名。）

可以同时使用这两个规则。
给定电子邮件列表 emails，我们会向列表中的每个地址发送一封电子邮件。实际收到邮件的不同地址有多少？

### 测试用例
["test.email+alex@leetcode.com","test.e.mail+bob.cathy@leetcode.com","testemail+david@lee.tcode.com"]

### 代码

Python

``` Python
class Solution(object):
    def numUniqueEmails(self, emails):
        """
        :type emails: List[str]
        :rtype: int
        """
        email_list = []
        for email in emails:
            local, remote = email.split("@")
            if "+" in local:
                local = local.split("+")[0]
            if "." in local:
                local = local.replace(".", "")
            email_list.append(local + "@" + remote)
        return len(set(email_list))
        
# 另一种：
class Solution(object):
    def numUniqueEmails(self, emails):
        """
        :type emails: List[str]
        :rtype: int
        """
        email_list = []
        for email in emails:
            local, remote = email.split("@")
            index = local.find('+')
            local = local[:index]
            if "." in local:
                local = local.replace(".", "")
            email_list.append(local + "@" + remote)
        return len(set(email_list))
```

Java

``` Java
class Solution {
    public int numUniqueEmails(String[] emails) {
        HashSet<String> strings = new HashSet<>();
        for (String email : emails) {
            int plusPos = email.indexOf("+");
            int twoPos = email.indexOf("@");
 
            String substring = email.substring(0, plusPos);
            String substring1 = email.substring(twoPos, email.length());
            strings.add(substring.replace(".", "") + substring1);
            
        }
        return strings.size();
    }
}
```

## 题目3
给定一个非负整数 num，反复将各个位上的数字相加，直到结果为一位数。

示例:
输入: 38
输出: 2 
解释: 各位相加的过程为：3 + 8 = 11, 1 + 1 = 2。 由于 2 是一位数，所以返回 2。

进阶:
你可以不使用循环或者递归，且在 O(1) 时间复杂度内解决这个问题吗？

### 测试用例
38
1298

### 代码

``` Python
class Solution(object):
    def addDigits(self, num):
        """
        :type num: int
        :rtype: int
        """
        # 一般方式
        while num>9:
            num1=0
            for i in str(num):
                num1+=int(i)
            num=num1
        return num
        
        # 利用reduce以及匿名函数
        while num > 9:
            temp = list(str(num))
            num = reduce(lambda x, y: int(x) + int(y), temp)
        return num
        
        # 利用sum和map函数
        while num>9:
            num  = sum(map(int,list(str(num))))
        return num

        # 最简单的这样
        return (num-1)%9+1
```