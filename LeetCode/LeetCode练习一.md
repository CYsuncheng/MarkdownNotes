# LeetCode练习一

## 重复 N 次的元素
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

## 独特的电子邮件地址
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
        
# 另一种（比上面的快了4ms）：
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

## 各位相加
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
```

## 按奇偶排序数组
给定一个非负整数数组 A，返回一个由 A 的所有偶数元素组成的数组，后面跟 A 的所有奇数元素。
你可以返回满足此条件的任何数组作为答案。
示例：
输入：[3,1,2,4]
输出：[2,4,3,1]
输出 [4,2,3,1]，[2,4,1,3] 和 [4,2,1,3] 也会被接受。

### 测试用例
[3,1,2,4,6,7,9,8]

### 代码

``` Python
class Solution(object):
    def sortArrayByParity(self, A):
        """
        :type A: List[int]
        :rtype: List[int]
        """
        o_list = []
        n_list = []
        for num in A:
            if num%2 == 0:
                o_list.append(num)
            else:
                n_list.append(num)
        return o_list + n_list
```

## 按奇偶排序数组 II 
给定一个非负整数数组 A， A 中一半整数是奇数，一半整数是偶数。
对数组进行排序，以便当 A[i] 为奇数时，i 也是奇数；当 A[i] 为偶数时， i 也是偶数。
你可以返回任何满足上述条件的数组作为答案。

### 测试用例
[2,4,6,8,5,3,1,7,4,6,8,2,5,3,7,1]

### 代码

``` Python
class Solution(object):
    def sortArrayByParityII(self, A):
        """
        :type A: List[int]
        :rtype: List[int]
        """
        list_ji = []
        list_ou = []
        result_list = []
        for num in A:
            if num%2 == 0:
                list_ou.append(num)
            else:
                list_ji.append(num)
        for i in range(len(list_ou)) :
            result_list.append(list_ou[i])
            result_list.append(list_ji[i])
        return result_list
```

## 机器人能否返回原点
在二维平面上，有一个机器人从原点 (0, 0) 开始。给出它的移动顺序，判断这个机器人在完成移动后是否在 (0, 0) 处结束。
移动顺序由字符串表示。字符 move[i] 表示其第 i 次移动。机器人的有效动作有 R（右），L（左），U（上）和 D（下）。如果机器人在完成所有动作后返回原点，则返回 true。否则，返回 false。
注意：机器人“面朝”的方向无关紧要。 “R” 将始终使机器人向右移动一次，“L” 将始终向左移动等。此外，假设每次移动机器人的移动幅度相同。

示例 1:
输入: "UD"
输出: true
解释：机器人向上移动一次，然后向下移动一次。所有动作都具有相同的幅度，因此它最终回到它开始的原点。因此，我们返回 true。

示例 2:
输入: "LL"
输出: false
解释：机器人向左移动两次。它最终位于原点的左侧，距原点有两次 “移动” 的距离。我们返回 false，因为它在移动结束时没有返回原点。

### 测试用例
"ULLLRRRD"

### 代码
Python

``` Python
class Solution(object):
    def judgeCircle(self, moves):
        """
        :type moves: str
        :rtype: bool
        """
        return moves.count('L') == moves.count('R') and moves.count('U') == moves.count('D')
```

Java

``` Java
class Solution {
    public boolean judgeCircle(String moves) {
        char[] array = moves.toCharArray();
        int level = 0;
        int vertical = 0;
        for(int i = 0; i < array.length; i++) {
            if(array[i] == 'R') {
                level++;
            } else if(array[i] == 'L') {
                level--;
            } else if(array[i] == 'U') {
                vertical++;
            } else if(array[i] == 'D') {
                vertical--;
            }
        }
        if(level == 0 && vertical == 0) {
            return true;
        } else {
            return false;
        }      
    }
}
```

## 山脉数组的峰顶索引
我们把符合下列属性的数组 A 称作山脉：
1. A.length >= 3
2. 存在 0 < i < A.length - 1 使得A[0] < A[1] < ... A[i-1] < A[i] > A[i+1] > ... > A[A.length - 1]

给定一个确定为山脉的数组，返回任何满足 A[0] < A[1] < ... A[i-1] < A[i] > A[i+1] > ... > A[A.length - 1] 的 i 的值。

示例 1：
输入：[0,1,0]
输出：1

示例 2：
输入：[0,2,1,0]
输出：1 

### 测试用例
[0,2,1,0]
[0,1,3,4,2,1]

### 代码
``` Python
# 这个看题目有些绕，其实分析下来，就是这个列表中间的某一项是最大值，只要找到这个值的索引位置就对了
class Solution(object):
    def peakIndexInMountainArray(self, A):
        """
        :type A: List[int]
        :rtype: int
        """
        return A.index(max(A))
```

## 二叉树的最大深度
二叉树的深度为根节点到最远叶子节点的最长路径上的节点数。
说明: 叶子节点是指没有子节点的节点。

### 测试用例
[3,9,20,null,null,15,7]

### 代码

``` Python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution:
    def maxDepth(self, root):
        """
        :type root: TreeNode
        :rtype: int
        """ 
        if root is None: 
            return 0 
        else: 
            left_height = self.maxDepth(root.left) 
            right_height = self.maxDepth(root.right) 
            return max(left_height, right_height) + 1 
```

## 斐波那契数
通常用 F(n) 表示，形成的序列称为斐波那契数列。该数列由 0 和 1 开始，后面的每一项数字都是前面两项数字的和。也就是：
F(0) = 0,   F(1) = 1
F(N) = F(N - 1) + F(N - 2), 其中 N > 1.
给定 N，计算 F(N)。

### 测试用例
9

### 代码

``` Python
class Solution(object):
    def fib(self, N):
        """
        :type N: int
        :rtype: int
        """
        if N == 0:
            return 0
        elif N == 1:
            return 1
        else:
            return self.fib(N -1) + self.fib(N -2)
```

## 自除数 
自除数 是指可以被它包含的每一位数除尽的数。
例如，128 是一个自除数，因为 128 % 1 == 0，128 % 2 == 0，128 % 8 == 0。
还有，自除数不允许包含 0 。
给定上边界和下边界数字，输出一个列表，列表的元素是边界（含边界）内所有的自除数。

### 测试用例
1，33

### 代码

Python

``` Python
class Solution(object):
    def selfDividingNumbers(self, left, right):
        """
        :type left: int
        :type right: int
        :rtype: List[int]
        """
        result = []
        for i in range(left, right+1):
            if "0" in str(i):
                continue
            for num in str(i):
                if i % int(num) != 0:
                    break;
            else:
                result.append(i)
        return result
```

Java

``` Java
class Solution {
    public List<Integer> selfDividingNumbers(int left, int right) {
        List<Integer> result=new ArrayList<>();
        while(left<=right){
            if(this.isSelfDividingNumber(left))
                result.add(left);
            left++;
        }
        return result;
    }
    public boolean isSelfDividingNumber(int n){
        int pivot=n;
        int divide;
        while(pivot>0){
            divide=pivot%10;
            if(divide==0||n%divide!=0)
                return false;
            pivot=pivot/10;
        }
        return true;
    }
}
```

