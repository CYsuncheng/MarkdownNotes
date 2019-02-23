# LeetCode练习三

## 给定一个单词列表，只返回可以使用在键盘同一行的字母打印出来的单词。

### 测试用例
输入: ["Hello", "Alaska", "Dad", "Peace"]
输出: ["Alaska", "Dad"]

### 代码
``` Python
class Solution:
        def findWords(self, words):
            """
            :type words: List[str]
            :rtype: List[str]
            """
            lis = []
            s1 = 'qwertyuiopQWERTYUIOP'
            s2 = 'asdfghjklASDFGHJKL'
            s3 = 'zxcvbnmZXCVBNM'
            
            for word in words:
                if word[0] in s1:
                    for i in range(1, len(word)):
                        if word[i] in s1:
                            continue
                        else:
                            break
                    else:
                        lis.append(word)
                elif word[0] in s2:
                    for i in range(1, len(word)):
                        if word[i] in s2:
                            continue
                        else:
                            break
                    else:
                        lis.append(word)
                elif word[0] in s3:
                    for i in range(1, len(word)):
                        if word[i] in s3:
                            continue
                        else:
                            break
                    else:
                        lis.append(word)
            return lis
```

## 最大连续1的个数
给定一个二进制数组， 计算其中最大连续1的个数。

注意：
输入的数组只包含 0 和1。
输入数组的长度是正整数，且不超过 10,000。

### 测试用例
输入: [1,1,0,1,1,1]
输出: 3
解释: 开头的两位和最后的三位都是连续1，所以最大连续1的个数是 3

### 代码

``` Python
class Solution(object):
    def findMaxConsecutiveOnes(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        res = 0
        fin_res = 0
        for n in nums:
            if n == 1:
                res += 1
                if fin_res > res:
                    fin_res = fin_res
                else:
                    fin_res = res
            else:
                res = 0
        return fin_res
```

## 给定一个数组 nums，编写一个函数将所有 0 移动到数组的末尾，同时保持非零元素的相对顺序。

说明:
必须在原数组上操作，不能拷贝额外的数组。
尽量减少操作次数。

### 测试用例
输入: [0,1,0,3,12]
输出: [1,3,12,0,0]

### 代码

``` Python
class Solution(object):
    def moveZeroes(self, nums):
        """
        :type nums: List[int]
        :rtype: void Do not return anything, modify nums in-place instead.
        """
        count = 0
        for i in range(0, len(nums)):
            if (nums[i] != 0):
                nums[count] = nums[i]
                count += 1
        for j in range(count, len(nums)):
            nums[j] = 0
```

## 作为该电影院的信息部主管，您需要编写一个 SQL查询，找出所有影片描述为非 boring (不无聊) 的并且 id 为奇数 的影片，结果请按等级 rating 排列。

例如：
![](https://ws4.sinaimg.cn/large/006tKfTcly1g0fan67a7rj30wu0p2mzz.jpg)

``` SQl
# Write your MySQL query statement below
select * from cinema where description!='boring' and id%2!=0 order by rating desc
```

## 给定一个非空的字符串，判断它是否可以由它的一个子串重复多次构成。给定的字符串只含有小写英文字母，并且长度不超过10000。

示例 1:
输入: "abab"
输出: True
解释: 可由子字符串 "ab" 重复两次构成。

示例 2:
输入: "aba"
输出: False

示例 3:
输入: "abcabcabcabc"
输出: True
解释: 可由子字符串 "abc" 重复四次构成。 (或者子字符串 "abcabc" 重复两次构成。)

### 代码
``` Python
class Solution(object):
    def repeatedSubstringPattern(self, s):
        """
        :type s: str
        :rtype: bool
        """
        result = []
        for i in range(1,len(s)/2+1):
            if s[i] == s[0]:
                result.append(i)

        for i in result:
            if s[:i]*(len(s)/i) == s:
                return True
        return False
```