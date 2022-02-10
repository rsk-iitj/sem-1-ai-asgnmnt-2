import sys
import queue
from collections import deque
from curses.ascii import isalpha

# Check if the expression is WFF or Not.
def _check_if_well_formed_(inp_str: str):
    i =0
    operators="~&>|"
    alloperators="!~&>|"
    special_characters = "@#$%^*()-+?_=,</"
    if any(c in special_characters for c in inp_str):
        return "Not Well Formed Formula" 
    if inp_str[0] in operators:
        return "Not Well Formed Formula" 
    if len(inp_str)==1 and inp_str[0] in alloperators:
        return "Not Well Formed Formula"
    if inp_str[len(inp_str)-1] in operators or inp_str[len(inp_str)-1] =='!' :
        return "Not Well Formed Forumla"
    while i<len(inp_str)-1:
        char = inp_str[i]
        nextchar = inp_str[i+1]
        if char in  operators and nextchar in operators:
            return "Not Well Formed Formula"
        if isalpha(char) and isalpha(nextchar):
            return "Not Well Formed Formula" 
        if len(inp_str)>=3 and i+1 <= len(inp_str)-1 and isalpha(char) and nextchar =='!' and isalpha(inp_str[i+2]):
            return "Not Well Formed Formula" 
        if len(inp_str)>=4 and i+2 <= len(inp_str)-1:
            nextNextChar=inp_str[i+2]
            if char=='>' and nextNextChar=='>':
                return "Not Well Formed Formula"
        i+=1
    return "Well formed"  

class ExpTreeNode(object):
    def __init__(self, data):
        self.data = data
        self.right = None
        self.left = None
        # flag for operators to distinguish from operands
        self.operator = False
    
    def __repr__(self) -> str:
        """Return a string representation of this parse tree node."""
        return 'ParseTreeNode({!r})'.format(self.data)

    def is_leaf(self) -> bool:
        """Return True if this node is a leaf(that is operand)."""
        return self.left is None and self.right is None


class ExpressionTree(object):
    def __init__(self, expression: str = None):
        self.root = None
        self.size = 0

        if expression is not None:
            self._insert_in_tree_(expression)

    def __repr__(self) -> str:
        """Return a string representation of this binary search tree."""
        return 'BinarySearchTree({} nodes)'.format(self.size)

    def is_empty(self) -> bool:
        """Return True if this binary search tree is empty (has no nodes)."""
        return self.root is None

    def _insert_in_tree_(self, expression: str):
        postfix_expression = self.convert_infix_postfix(expression)
        #print(postfix_exp)
        stack_nodes = deque()
        char = postfix_expression[0]
        node = ExpTreeNode(char)
       
        #print(len(postfix_exp))
        if len(postfix_expression) ==1:
            self.root=node
            self.size += 1
        else:
            stack_nodes.appendleft(node)
            # iterator for expression
            i = 1
            #print("Lenth of stack")
            #print(len(stack))
            while len(stack_nodes) != 0:
                char = postfix_expression[i]
                if "!" in char:
                    node = ExpTreeNode(char)
                    stack_nodes.appendleft(node)
                elif isalpha(char):
                    node = ExpTreeNode(char)
                    stack_nodes.appendleft(node)
                else:
                    operator_root = ExpTreeNode(char)
                    operator_root.operator = True
                    right_child = stack_nodes.popleft()
                    left_child = stack_nodes.popleft()
                    operator_root.right = right_child
                    operator_root.left = left_child
                    stack_nodes.appendleft(operator_root)
                    if len(stack_nodes) == 1 and i == len(postfix_expression) - 1:
                        self.root = stack_nodes.popleft()
                i += 1
                self.size += 1
            #print(f"i is {i} in insert ")
    
    def _print_inorder_travsersal(self) -> list:
        """Return an in-order list of all items in this binary search tree."""
        items = []
        if not self.is_empty():
            if self.root.left is None and self.root.right is None:
                items.append(self.root.data)
            else:
                self._traverse_inorder_(self.root, items.append)
        return items

    def _traverse_inorder_(self, node, visit):
        if(node):
            self._traverse_inorder_(node.left, visit)
            visit(node.data)
            self._traverse_inorder_(node.right, visit)

    def convert_infix_postfix(self, infix_input: list) -> list:
        operator_precedence= {'!': 5, '&': 4, '|':3, '>': 2, '~': 1 }
        associativity = {'!': "LR", '&': "LR", '>': "LR", '~': "LR", '|': "LR"}
        # clean the infix expression
        clean_infix = self._clean_user_input(infix_input)
        #print(clean_infix)
        i = 0
        postfix_exp = []
        operators = "&>|~"
        stack = deque()
        while i < len(clean_infix):
            char = clean_infix[i]
            #print(f"char: {char}")
            if char in operators:
                if len(stack) == 0 or stack[0] == '(':
                    stack.appendleft(char)
                    i += 1
                else:
                    top_item = stack[0]
                    if operator_precedence[char] == operator_precedence[top_item]:
                        if associativity[char] == "LR":
                            popped_item = stack.popleft()
                            postfix_exp.append(popped_item)
                        elif associativity[char] == "RL":
                            stack.appendleft(char)
                            i += 1
                    elif operator_precedence[char] > operator_precedence[top_item]:
                        stack.appendleft(char)
                        i += 1
                    elif operator_precedence[char] < operator_precedence[top_item]:
                        popped_item = stack.popleft()
                        postfix_exp.append(popped_item)
            #For case when already braces are there in expression.             
            elif char == '(':
                stack.appendleft(char)
                i += 1
            elif char == ')':
                top_item = stack[0]
                while top_item != '(':
                    popped_item = stack.popleft()
                    postfix_exp.append(popped_item)
                    top_item = stack[0]
                stack.popleft()
                i += 1
            else:
                postfix_exp.append(char)
                i += 1
            # print(postfix)
            # print(f"stack: {stack}")
        
        if len(stack) > 0:
            for i in range(len(stack)):
                postfix_exp.append(stack.popleft())
        # while len(stack) > 0:
        #     postfix.append(stack.popleft())
        #print(postfix)
        return postfix_exp
        
    def _clean_user_input(self, infix_exp: str) -> list:
        # remove all whitespaces
        clean_exp = "".join(infix_exp.split())
        #print(f"clean_exp: {clean_exp}")
        formated_exp = []
        i = 0
        while i < len(clean_exp):
            char = clean_exp[i]
            #print(char)
            if char =='!':
                next_char=clean_exp[i+1]
                thischar = char + next_char    
                formated_exp.append(thischar)
                i+=2
            else:
                formated_exp.append(char)
                i += 1
        #print(formated_exp)
        return formated_exp
  
            
    def _add_parenthesis_exp(self, node=None) -> str:
        if node is None:
            node = self.root
        # check if we are at the leaf, it means it is a operand
        if node is None:
           return None
        if node.is_leaf():
            val = node.data
            if '!' in val:
                return '('+val+')'
            else:
                return val
        
        left_value = self._add_parenthesis_exp(node.left)
        right_value = self._add_parenthesis_exp(node.right)
        
        operators = "&~!|>"
        if node.data in operators:
            return '('+left_value + node.data +right_value+')'
        else:
            return left_value + right_value

def main():
    user_input = input("Enter the Expression:")
    if _check_if_well_formed_(user_input) == "Well formed":
        tree_obj = ExpressionTree(user_input)
        #print(f"Tree: {tree_obj}")
        #print(tree_obj._print_inorder_travsersal())
        str = tree_obj._add_parenthesis_exp()
        #print(str)
        if len(str)==1: 
            print(str)
        else:
            print(str[1:-1])
    else:
        print("Not Well Formed Formula")

if __name__ == "__main__":
    main()