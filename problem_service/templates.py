TEMPLATES = {
    "two-sum": {
        "python": """
# Input parsing
def parse_input():
    nums = list(map(int, input().strip('[]').split(',')))
    target = int(input())
    return nums, target

# Solution class
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        # Your solution here
        pass

# Main execution
if __name__ == "__main__":
    nums, target = parse_input()
    solution = Solution()
    result = solution.twoSum(nums, target)
    print(result)
""",
        "cpp": """
#include <vector>
#include <iostream>
#include <string>
#include <sstream>
using namespace std;

// Input parsing
pair<vector<int>, int> parse_input() {
    string line;
    getline(cin, line);
    line = line.substr(1, line.size() - 2); // Remove []
    stringstream ss(line);
    vector<int> nums;
    string num;
    while (getline(ss, num, ',')) {
        nums.push_back(stoi(num));
    }
    int target;
    cin >> target;
    return {nums, target};
}

class Solution {
public:
    vector<int> twoSum(vector<int>& nums, int target) {
        // Your solution here
    }
};

int main() {
    auto [nums, target] = parse_input();
    Solution solution;
    vector<int> result = solution.twoSum(nums, target);
    cout << "[" << result[0] << "," << result[1] << "]" << endl;
    return 0;
}
"""
    },
    "add-two-numbers": {
        "python": """
# ListNode class
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

# Input parsing
def parse_input():
    l1_str = input().strip('[]').split(',')
    l2_str = input().strip('[]').split(',')
    
    def create_list(lst_str):
        if not lst_str or lst_str[0] == '': return None
        head = ListNode(int(lst_str[0]))
        current = head
        for val in lst_str[1:]:
            current.next = ListNode(int(val))
            current = current.next
        return head
    
    return create_list(l1_str), create_list(l2_str)

class Solution:
    def addTwoNumbers(self, l1: ListNode, l2: ListNode) -> ListNode:
        # Your solution here
        pass

if __name__ == "__main__":
    l1, l2 = parse_input()
    solution = Solution()
    result = solution.addTwoNumbers(l1, l2)
    
    # Print result
    output = []
    while result:
        output.append(str(result.val))
        result = result.next
    print("[" + ",".join(output) + "]")
""",
        "cpp": """
#include <vector>
#include <iostream>
#include <string>
#include <sstream>
using namespace std;

struct ListNode {
    int val;
    ListNode *next;
    ListNode() : val(0), next(nullptr) {}
    ListNode(int x) : val(x), next(nullptr) {}
    ListNode(int x, ListNode *next) : val(x), next(next) {}
};

pair<ListNode*, ListNode*> parse_input() {
    string line;
    getline(cin, line);
    line = line.substr(1, line.size() - 2);
    stringstream ss(line);
    ListNode* l1 = nullptr;
    ListNode* current = nullptr;
    string val;
    while (getline(ss, val, ',')) {
        if (!l1) {
            l1 = new ListNode(stoi(val));
            current = l1;
        } else {
            current->next = new ListNode(stoi(val));
            current = current->next;
        }
    }
    
    getline(cin, line);
    line = line.substr(1, line.size() - 2);
    stringstream ss2(line);
    ListNode* l2 = nullptr;
    current = nullptr;
    while (getline(ss2, val, ',')) {
        if (!l2) {
            l2 = new ListNode(stoi(val));
            current = l2;
        } else {
            current->next = new ListNode(stoi(val));
            current = current->next;
        }
    }
    return {l1, l2};
}

class Solution {
public:
    ListNode* addTwoNumbers(ListNode* l1, ListNode* l2) {
        // Your solution here
    }
};

int main() {
    auto [l1, l2] = parse_input();
    Solution solution;
    ListNode* result = solution.addTwoNumbers(l1, l2);
    
    cout << "[";
    while (result) {
        cout << result->val;
        if (result->next) cout << ",";
        result = result->next;
    }
    cout << "]" << endl;
    return 0;
}
"""
    },
    "longest-substring-without-repeating-characters": {
        "python": """
# Input parsing
def parse_input():
    return input().strip('"')

class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        # Your solution here
        pass

if __name__ == "__main__":
    s = parse_input()
    solution = Solution()
    result = solution.lengthOfLongestSubstring(s)
    print(result)
""",
        "cpp": """
#include <string>
#include <iostream>
using namespace std;

string parse_input() {
    string s;
    getline(cin, s);
    return s.substr(1, s.size() - 2); // Remove quotes
}

class Solution {
public:
    int lengthOfLongestSubstring(string s) {
        // Your solution here
    }
};

int main() {
    string s = parse_input();
    Solution solution;
    int result = solution.lengthOfLongestSubstring(s);
    cout << result << endl;
    return 0;
}
"""
    },
    "median-of-two-sorted-arrays": {
        "python": """
# Input parsing
def parse_input():
    nums1 = list(map(int, input().strip('[]').split(',')))
    nums2 = list(map(int, input().strip('[]').split(',')))
    return nums1, nums2

class Solution:
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        # Your solution here
        pass

if __name__ == "__main__":
    nums1, nums2 = parse_input()
    solution = Solution()
    result = solution.findMedianSortedArrays(nums1, nums2)
    print(result)
""",
        "cpp": """
#include <vector>
#include <iostream>
#include <string>
#include <sstream>
using namespace std;

pair<vector<int>, vector<int>> parse_input() {
    string line;
    getline(cin, line);
    line = line.substr(1, line.size() - 2);
    stringstream ss(line);
    vector<int> nums1;
    string num;
    while (getline(ss, num, ',')) {
        nums1.push_back(stoi(num));
    }
    
    getline(cin, line);
    line = line.substr(1, line.size() - 2);
    stringstream ss2(line);
    vector<int> nums2;
    while (getline(ss2, num, ',')) {
        nums2.push_back(stoi(num));
    }
    return {nums1, nums2};
}

class Solution {
public:
    double findMedianSortedArrays(vector<int>& nums1, vector<int>& nums2) {
        // Your solution here
    }
};

int main() {
    auto [nums1, nums2] = parse_input();
    Solution solution;
    double result = solution.findMedianSortedArrays(nums1, nums2);
    cout << result << endl;
    return 0;
}
"""
    },
    "longest-palindromic-substring": {
        "python": """
# Input parsing
def parse_input():
    return input().strip('"')

class Solution:
    def longestPalindrome(self, s: str) -> str:
        # Your solution here
        pass

if __name__ == "__main__":
    s = parse_input()
    solution = Solution()
    result = solution.longestPalindrome(s)
    print('"' + result + '"')
""",
        "cpp": """
#include <string>
#include <iostream>
using namespace std;

string parse_input() {
    string s;
    getline(cin, s);
    return s.substr(1, s.size() - 2); // Remove quotes
}

class Solution {
public:
    string longestPalindrome(string s) {
        // Your solution here
    }
};

int main() {
    string s = parse_input();
    Solution solution;
    string result = solution.longestPalindrome(s);
    cout << "\"" << result << "\"" << endl;
    return 0;
}
"""
    },
    "zigzag-conversion": {
        "python": """
# Input parsing
def parse_input():
    s = input().strip('"')
    numRows = int(input())
    return s, numRows

class Solution:
    def convert(self, s: str, numRows: int) -> str:
        # Your solution here
        pass

if __name__ == "__main__":
    s, numRows = parse_input()
    solution = Solution()
    result = solution.convert(s, numRows)
    print('"' + result + '"')
""",
        "cpp": """
#include <string>
#include <iostream>
using namespace std;

pair<string, int> parse_input() {
    string s;
    getline(cin, s);
    s = s.substr(1, s.size() - 2); // Remove quotes
    int numRows;
    cin >> numRows;
    return {s, numRows};
}

class Solution {
public:
    string convert(string s, int numRows) {
        // Your solution here
    }
};

int main() {
    auto [s, numRows] = parse_input();
    Solution solution;
    string result = solution.convert(s, numRows);
    cout << "\"" << result << "\"" << endl;
    return 0;
}
"""
    },
    "reverse-integer": {
        "python": """
# Input parsing
def parse_input():
    return int(input())

class Solution:
    def reverse(self, x: int) -> int:
        # Your solution here
        pass

if __name__ == "__main__":
    x = parse_input()
    solution = Solution()
    result = solution.reverse(x)
    print(result)
""",
        "cpp": """
#include <iostream>
using namespace std;

int parse_input() {
    int x;
    cin >> x;
    return x;
}

class Solution {
public:
    int reverse(int x) {
        // Your solution here
    }
};

int main() {
    int x = parse_input();
    Solution solution;
    int result = solution.reverse(x);
    cout << result << endl;
    return 0;
}
"""
    },
    "string-to-integer-atoi": {
        "python": """
# Input parsing
def parse_input():
    return input().strip('"')

class Solution:
    def myAtoi(self, s: str) -> int:
        # Your solution here
        pass

if __name__ == "__main__":
    s = parse_input()
    solution = Solution()
    result = solution.myAtoi(s)
    print(result)
""",
        "cpp": """
#include <string>
#include <iostream>
using namespace std;

string parse_input() {
    string s;
    getline(cin, s);
    return s.substr(1, s.size() - 2); // Remove quotes
}

class Solution {
public:
    int myAtoi(string s) {
        // Your solution here
    }
};

int main() {
    string s = parse_input();
    Solution solution;
    int result = solution.myAtoi(s);
    cout << result << endl;
    return 0;
}
"""
    },
    "palindrome-number": {
        "python": """
# Input parsing
def parse_input():
    return int(input())

class Solution:
    def isPalindrome(self, x: int) -> bool:
        # Your solution here
        pass

if __name__ == "__main__":
    x = parse_input()
    solution = Solution()
    result = solution.isPalindrome(x)
    print("true" if result else "false")
""",
        "cpp": """
#include <iostream>
using namespace std;

int parse_input() {
    int x;
    cin >> x;
    return x;
}

class Solution {
public:
    bool isPalindrome(int x) {
        // Your solution here
    }
};

int main() {
    int x = parse_input();
    Solution solution;
    bool result = solution.isPalindrome(x);
    cout << (result ? "true" : "false") << endl;
    return 0;
}
"""
    },
    "regular-expression-matching": {
        "python": """
# Input parsing
def parse_input():
    s = input().strip('"')
    p = input().strip('"')
    return s, p

class Solution:
    def isMatch(self, s: str, p: str) -> bool:
        # Your solution here
        pass

if __name__ == "__main__":
    s, p = parse_input()
    solution = Solution()
    result = solution.isMatch(s, p)
    print("true" if result else "false")
""",
        "cpp": """
#include <string>
#include <iostream>
using namespace std;

pair<string, string> parse_input() {
    string s, p;
    getline(cin, s);
    s = s.substr(1, s.size() - 2); // Remove quotes
    getline(cin, p);
    p = p.substr(1, p.size() - 2); // Remove quotes
    return {s, p};
}

class Solution {
public:
    bool isMatch(string s, string p) {
        // Your solution here
    }
};

int main() {
    auto [s, p] = parse_input();
    Solution solution;
    bool result = solution.isMatch(s, p);
    cout << (result ? "true" : "false") << endl;
    return 0;
}
"""
    }
} 