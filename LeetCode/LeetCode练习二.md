# LeetCode练习二

## 两数之和
给定一个整数数组 nums 和一个目标值 target，请你在该数组中找出和为目标值的那 两个 整数，并返回他们的数组下标。
你可以假设每种输入只会对应一个答案。但是，你不能重复利用这个数组中同样的元素。

### 测试用例：
nums = [2, 7, 11, 15], target = 9
返回 [0, 1]

### 代码

``` Python
class Solution:
    def twoSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        for i,n in enumerate(nums):
            if target-n in nums[i+1:]:
                return [i,nums[i+1:].index(target-n)+i+1]
```

``` Java
public int[] twoSum(int[] nums, int target) {
    Map<Integer, Integer> map = new HashMap<>();
    for (int i = 0; i < nums.length; i++) {
        int complement = target - nums[i];
        if (map.containsKey(complement)) {
            return new int[] { map.get(complement), i };
        }
        map.put(nums[i], i);
    }
    throw new IllegalArgumentException("No two sum solution");
}
```

## 反转字符串中的单词 III
给定一个字符串，你需要反转字符串中每个单词的字符顺序，同时仍保留空格和单词的初始顺序。

示例 1:
输入: "Let's take LeetCode contest"
输出: "s'teL ekat edoCteeL tsetnoc" 
注意：在字符串中，每个单词由单个空格分隔，并且字符串中不会有任何额外的空格。

### 测试用例
"Let's take LeetCode contest"

### 代码

``` Python
class Solution(object):
    def reverseWords(self, s):
        """
        :type s: str
        :rtype: str
        """
        return " ".join(x[::-1] for x in s.split())
```

## 子域名访问计数
一个网站域名，如"discuss.leetcode.com"，包含了多个子域名。作为顶级域名，常用的有"com"，下一级则有"leetcode.com"，最低的一级为"discuss.leetcode.com"。当我们访问域名"discuss.leetcode.com"时，也同时访问了其父域名"leetcode.com"以及顶级域名 "com"。
给定一个带访问次数和域名的组合，要求分别计算每个域名被访问的次数。其格式为访问次数+空格+地址，例如："9001 discuss.leetcode.com"。
接下来会给出一组访问次数和域名组合的列表cpdomains 。要求解析出所有域名的访问次数，输出格式和输入格式相同，不限定先后顺序。

示例
输入: 
["900 google.mail.com", "50 yahoo.com", "1 intel.mail.com", "5 wiki.org"]
输出: 
["901 mail.com","50 yahoo.com","900 google.mail.com","5 wiki.org","5 org","1 intel.mail.com","951 com"]
说明: 
按照假设，会访问"google.mail.com" 900次，"yahoo.com" 50次，"intel.mail.com" 1次，"wiki.org" 5次。
而对于父域名，会访问"mail.com" 900+1 = 901次，"com" 900 + 50 + 1 = 951次，和 "org" 5 次。

### 测试用例
["900 google.mail.com", "50 yahoo.com", "1 intel.mail.com", "5 wiki.org"]

### 代码

``` Python
class Solution(object):
    def subdomainVisits(self, cpdomains):
        """
        :type cpdomains: List[str]
        :rtype: List[str]
        """
        res_map = {}

        for i in cpdomains:
            temp_result = i.split()
            num = int(temp_result[0])
            addr = temp_result[1]
            if addr in res_map:
                res_map[addr] += num
            else:
                res_map[addr] = num

            while '.' in addr:
                addr = addr[addr.index('.') + 1:]
                if addr in res_map:
                    res_map[addr] += num
                else:
                    res_map[addr] = num

        return [str(res_map[key]) + ' ' + key for key in res_map]
```

## 岛屿的周长
给定一个包含 0 和 1 的二维网格地图，其中 1 表示陆地 0 表示水域。
网格中的格子水平和垂直方向相连（对角线方向不相连）。整个网格被水完全包围，但其中恰好有一个岛屿（或者说，一个或多个表示陆地的格子相连组成的岛屿）。
岛屿中没有“湖”（“湖” 指水域在岛屿内部且不和岛屿周围的水相连）。格子是边长为 1 的正方形。网格为长方形，且宽度和高度均不超过 100 。计算这个岛屿的周长。

示例 :
输入:
[[0,1,0,0],
 [1,1,1,0],
 [0,1,0,0],
 [1,1,0,0]]
输出: 16

### 测试用例
[[0,1,0,0],[1,1,1,0],[0,1,0,0],[1,1,0,0]]

### 代码
Python

``` Python
class Solution(object):
    def islandPerimeter(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: int
        """
        sum_grid = 0
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if grid[i][j] == 1:
                    sum_grid += 4
                    if (i > 0 and grid[i-1][j] == 1):
                        sum_grid -= 1
                    if (i < (len(grid) -1) and grid[i+1][j] == 1):
                        sum_grid -= 1
                    if (j > 0 and grid[i][j-1] == 1):
                        sum_grid -= 1
                    if (j < (len(grid[i]) -1) and grid[i][j+1] == 1):
                        sum_grid -= 1
        return sum_grid
```

Java

``` Java
class Solution {
    public int islandPerimeter(int[][] grid) {
        int num = 0;
        for(int i = 0; i < grid.length; i++) {
            for(int j = 0; j < grid[i].length; j++) {
                if(grid[i][j] == 1) {
                    num = num + 4;   
                    //如果grid[i+1][j]不超出数组并且也等于1（岛）则边减2
                    if(i + 1 < grid.length && grid[i + 1][j] == 1) {
                        num = num -2;
                    }
                    //如果grid[i][j+1]不超出数组并且也等于1（岛）则边减2
                    if(j + 1 < grid[i].length  && grid[i][j + 1] == 1) {
                        num = num -2;
                    }
                }
            }
        }
        return num;
    }
}
```

## Fizz Buzz
写一个程序，输出从 1 到 n 数字的字符串表示。
1. 如果 n 是3的倍数，输出“Fizz”；
2. 如果 n 是5的倍数，输出“Buzz”；
3. 如果 n 同时是3和5的倍数，输出 “FizzBuzz”。

### 测试用例
n = 15

### 代码

Python

``` Python
class Solution(object):
    def fizzBuzz(self, n):
        """
        :type n: int
        :rtype: List[str]
        """
        str_list = []
        for number in range(1, n+1):
            str_list.append(str(number))
            if number%3 == 0 and number%5 == 0:
                str_list[number-1] = "FizzBuzz"
            elif number%3 == 0:
                str_list[number-1] = "Fizz"
            elif number%5 == 0:
                str_list[number-1] = "Buzz"
        return str_list
```

Java

``` Java
class Solution {
    public List<String> fizzBuzz(int n) {
        List<String> result = new ArrayList<>();
        for (int i = 1; i <= n; i++) {
            if(i % 3 == 0 && i % 5 == 0){
                result.add("FizzBuzz");
            }else if(i % 3 == 0){
                result.add("Fizz");
            }else if(i % 5 == 0){
                result.add("Buzz");
            }else{
                result.add(i + "");
            }
        }
        return result;
    }
}
```

## 分糖果
给定一个偶数长度的数组，其中不同的数字代表着不同种类的糖果，每一个数字代表一个糖果。你需要把这些糖果平均分给一个弟弟和一个妹妹。返回妹妹可以获得的最大糖果的种类数。

示例 1:
输入: candies = [1,1,2,2,3,3]
输出: 3
解析: 一共有三种种类的糖果，每一种都有两个。
     最优分配方案：妹妹获得[1,2,3],弟弟也获得[1,2,3]。这样使妹妹获得糖果的种类数最多。

示例 2 :
输入: candies = [1,1,2,3]
输出: 2
解析: 妹妹获得糖果[2,3],弟弟获得糖果[1,1]，妹妹有两种不同的糖果，弟弟只有一种。这样使得妹妹可以获得的糖果种类数最多。

### 测试用例
[1,1,2,2,3,3]
[1,1,2,3]
[1,1,2,3,4,5,6,7,8,3,2,4]

### 代码

Python

``` Python
class Solution(object):
    def distributeCandies(self, candies):
        """
        :type candies: List[int]
        :rtype: int
        """
        r_set = set(candies)
        if len(r_set) >= len(candies)/2:
            return len(candies)/2
        else:
            return len(r_set)
            
        # 更简单的方式
        return min(len(candies)/2, len(set(candies)))
```

Java
 
``` Java
class Solution {
    public int distributeCandies(int[] candies) {
        Set set = new HashSet();
        for (int i=0; i<candies.length; i++) {
            set.add(candies[i]);
        }
        if (set.size() >= candies.length/2) {
            return candies.length/2;
        }
        else{
            return set.size();
        }
    }
}
```

## 下一个更大元素 I
给定两个没有重复元素的数组 nums1 和 nums2 ，其中nums1 是 nums2 的子集。找到 nums1 中每个元素在 nums2 中的下一个比其大的值。
nums1 中数字 x 的下一个更大元素是指 x 在 nums2 中对应位置的右边的第一个比 x 大的元素。如果不存在，对应位置输出-1。

示例 1:
输入: nums1 = [4,1,2], nums2 = [1,3,4,2].
输出: [-1,3,-1]
解释:
    对于num1中的数字4，你无法在第二个数组中找到下一个更大的数字，因此输出 -1。
    对于num1中的数字1，第二个数组中数字1右边的下一个较大数字是 3。
    对于num1中的数字2，第二个数组中没有下一个更大的数字，因此输出 -1。
    
### 测试用例
[4,1,2]
[1,3,4,2]
[4,1,2,5]
[1,3,4,2,5,6]

### 代码

``` Python
class Solution(object):
    def nextGreaterElement(self, findNums, nums):
        """
        :type findNums: List[int]
        :type nums: List[int]
        :rtype: List[int]
        """
        result = []
        for item in findNums:
            index = nums.index(item)
            if index < len(nums)-1: 
                for i in range(index, len(nums)-1):
                    if nums[i+1] > item:
                        result.append(nums[i+1])
                        break
                else:
                    result.append(-1)
            else:
                result.append(-1)
        return result
```

## 只出现一次的数字
给定一个非空整数数组，除了某个元素只出现一次以外，其余每个元素均出现两次。找出那个只出现了一次的元素。

### 测试用例
[4,1,2,1,2]

### 代码

**异或运算的运用，不太懂，先记下来**

``` Python
class Solution(object):
    def singleNumber(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        a = 0
        for num in nums:
            a = a ^ num
            print a
        return a
```

## 回文数
判断一个整数是否是回文数。回文数是指正序（从左向右）和倒序（从右向左）读都是一样的整数。

示例 1:
输入: 121
输出: true

示例 2:
输入: -121
输出: false
解释: 从左向右读, 为 -121 。 从右向左读, 为 121- 。因此它不是一个回文数。

### 测试用例
1234321

### 代码

``` Python
class Solution(object):
    def isPalindrome(self, x):
        """
        :type x: int
        :rtype: bool
        """
        if str(x) == str(x)[::-1]:
            return True
        return False
```

## 求众数
给定一个大小为 n 的数组，找到其中的众数。众数是指在数组中出现次数大于 ⌊ n/2 ⌋ 的元素。
你可以假设数组是非空的，并且给定的数组总是存在众数。
示例 1:
输入: [3,2,3]
输出: 3

示例 2:
输入: [2,2,1,1,1,2,2]
输出: 2

### 测试用例
[2,2,1,1,1,2,2]

### 代码

Python

``` Python
class Solution(object):
    def majorityElement(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        count = 1
        res = nums[0]
        for i in range(1, len(nums)):
            if res == nums[i]:
                count+=1
            else:
                count-=1
                if count == 0:
                    res = nums[i+1]
        return res
```

Java

``` Java
class Solution {
    public int majorityElement(int[] nums) {
		int count = 1;
		int maj = nums[0];
		for (int i = 1; i < nums.length; i++) {
			if (maj == nums[i])
				count++;
			else {
				count--;
				if (count == 0) {
					maj = nums[i + 1];
				}
			}
		}
		return maj;
	}
}
```

## 找不同
给定两个字符串 s 和 t，它们只包含小写字母。
字符串 t 由字符串 s 随机重排，然后在随机位置添加一个字母。
请找出在 t 中被添加的字母。

### 测试用例
"abcddddddddd"
"abcdedddddddd"

### 代码

``` Python
class Solution(object):
    def findTheDifference(self, s, t):
        """
        :type s: str
        :type t: str
        :rtype: str
        """
        for t_t in t:
            if t_t not in s:
                return t_t
        else:
            # 这个方法可以直接返回一个字典
            # from collections import Counter
            # s_dict = Counter(s)
            # t_dict = Counter(t)
            s_dict = {}
            t_dict = {}
            for s_k in s:
                s_dict[s_k] = s_dict.get(s_k, 0) + 1
            for t_k in t:
                t_dict[t_k] = t_dict.get(t_k, 0) + 1
        for k, v in s_dict.items():
            if t_dict[k] > v:
                return k
```

## 无重复字符的最长子串
给定一个字符串，请你找出其中不含有重复字符的 最长子串 的长度。

示例 1:
输入: "abcabcbb"
输出: 3 
解释: 因为无重复字符的最长子串是 "abc"，所以其长度为 3。

示例 2:
输入: "bbbbb"
输出: 1
解释: 因为无重复字符的最长子串是 "b"，所以其长度为 1。

示例 3:
输入: "pwwkew"
输出: 3
解释: 因为无重复字符的最长子串是 "wke"，所以其长度为 3。
     请注意，你的答案必须是 子串 的长度，"pwke" 是一个子序列，不是子串。
     
### 测试用例

``` Java
"abcdefghijklmnopqrstuvwxyzABCDabcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~abcdefghijklmnopqrstuvwxyzABCDabcdefghijklmnopqrstuvwxyzABCDabcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~ abcdefghijklmnopqrstuvwxyzABCDabcdefghijklmnopqrstuvwxyzABCDabcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~ abcdefghijklmnopqrstuvwxyzABCD"
```

### 代码

Java

``` Java
class Solution {
    public int lengthOfLongestSubstring(String s) {
        String maxSubString = "";
        String substring;
        for(int i=0;i<=s.length()-1;i++)
            for(int j=i+maxSubString.length();j<=s.length();j++){
                substring = s.substring(i,j);
                if(substring.length()>maxSubString.length()){
                    if(isNotContainSubString(substring)){
                        maxSubString = substring;
                    }else{
                        break;
                    }
                }
            }
        return maxSubString.length();
    }
    
    public boolean isNotContainSubString(String s){
        for(int i = 0;i<s.length();i++){
            String compareString = String.valueOf(s.charAt(i));
            String subString = s.substring(i+1);
            if(subString.contains(compareString)){
                return false;
            }else{
                if(i == s.length()-1)
                    return true;
            }
                
        }
            return false;    
    }
}
```

Python，运行OK，但是耗时久，不符合要求

``` Python
class Solution(object):
    def lengthOfLongestSubstring(self, s):
        """
        :type s: str
        :rtype: int
        """
        sub_str = []
        res = 0
        if s == "":
            return 0
        if s == " " or len(s) == 1:
            return 1
        for i in range(len(s)):
            for j in range(i+1, len(s)+1):
                sub = s[i:j]
                for s_s in sub:
                    if sub.count(s_s) == 1:
                        continue
                    else:
                        break
                else:
                    if res < j-i:
                        res = j-i
        return res
```