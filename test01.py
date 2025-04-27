from base import *
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next

class Solution:
    @pytest.makr.parametrize("l1,l2",[
        (build_list([2,4,3]),build_list([5,6,4]))
    ])
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        """
        数字逆序，直接遍历相夹
        判断是否进位
        进位则标记flag = 1
        每次相加时加上flag
        循环结果flag=1则添加一个节点
        """
        head = ListNode()
        cur = head
        flag = 0
        while l1 and l2:
            val = l1.val + l2.val + flag
            if val > 9:  # 进位
                flag = 1
                val = val % 10
            else:
                flag = 0
            l1 = l1.next
            l2 = l2.next
            cur.next = ListNode(val)
            cur = cur.next
        while l1:
            val = l1.val + flag
            if val > 9:
                flag = 1
                val %= 10
            else:
                flag = 0
            l1 = l1.next
            cur.next = ListNode(val)
            cur = cur.next
        while l2:
            val = l2.val + flag
            if val > 9:
                flag = 1
                val %= 10
            else:
                flag = 0
            l2 = l2.next
            cur.next = ListNode(val)
            cur = cur.next
        if flag:
            cur.next = ListNode(1)
        return head.next
