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
