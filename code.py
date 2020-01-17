def swap_if_left_less(arr,left,right):
    if arr[left] < arr[right]:
        t = arr[left]
        arr[left] = arr[right]
        arr[right] = t 
        return True
class Heap:
    def build_max_heap(self,arr):
        import math
        last_node_with_a_leaf_index = math.floor(len(arr)/2) - 1
        for i in range(last_node_with_a_leaf_index,-1,-1):
            self.max_heapify(i,arr)
        return arr
    def max_heapify(self,index,arr):
        if index == None:
            return
        left_child_index = self.left(index,arr)
        right_child_index = self.right(index,arr)
        if left_child_index and right_child_index:
            if arr[left_child_index] < arr[right_child_index]:
                if swap_if_left_less(arr,index,right_child_index):
                    self.max_heapify(right_child_index,arr)
            else:
                if swap_if_left_less(arr,index,left_child_index):
                    self.max_heapify(left_child_index,arr)            
        elif left_child_index:
            if swap_if_left_less(arr,index,left_child_index):
                self.max_heapify(left_child_index,arr)
    def left(self,index,arr):
        left_child_index = 2*(index+1) - 1
        if left_child_index <= len(arr) - 1:
            return left_child_index
        return None
    def right(self,index,arr):
        right_child_index = 2*(index+1)
        if right_child_index <= len(arr) - 1:
            return right_child_index
        return None   

def heap_sort(arr):
    heap = Heap()
    max_heap = heap.build_max_heap(arr)
    sorted_arr = []
    while max_heap:
        max = max_heap[0]
        max_heap[0] = max_heap[len(max_heap)-1]
        max_heap[len(max_heap)-1] = max
        sorted_arr.append(max_heap.pop())
        heap.max_heapify(0,max_heap)
    return sorted_arr

class BinarySearchTreeNode:
    def __init__(self,value):
        self.value = value
        self.left = None
        self.right = None
        self.parent = None
        self.size = 1
    def __repr__(self):
        return "("+str(self.value)+","+str(self.left)+","+str(self.right)+","+str(self.size)+")"

class BinarySearchTree:
    def __init__(self):
        self.root = None
    def insert(self,node):
        if not self.root:
            self.root = node
        else:
            self.compare_and_insert(self.root,node)
    def compare_and_insert(self,root,node):
        if root.value <= node.value and root.right == None:
            root.right = node
            node.parent = root
        elif root.value >= node.value and root.left == None:
            root.left = node
            node.parent = root
        elif root.value <= node.value:
            self.compare_and_insert(root.right,node)
        else:
            self.compare_and_insert(root.left,node)
        root.size += 1
    def delete(self,root,value):
        if root:
            if root.value == value:
                if root.parent:
                    root.parent.right = root.right
                    root.right.parent = root.parent
                    self.move_to_left_of(root.right,root.left)
                else:
                    self.root = root.right
                    root.right.parent = None
                    self.move_to_left_of(root.right,root.left)
                pass
            elif root.value > value:
                self.delete(root.left,value)
            elif root.value < value:
                self.delete(root.right,value)
    def move_to_left_of(self,tree,lessValueTree):
        if not tree.left:
            tree.left = lessValueTree
            lessValueTree.parent = tree
        else:
            self.move_to_left_of(tree.left,lessValueTree)
    def get_node(self,root,value):
        if root:
            if root.value == value:
                return root
            elif value > root.value:
                return self.get_node(root.right,value)
            else:
                return self.get_node(root.left,value)
    def next_larger(self,value):
        node = self.get_node(self.root,value)
        if node:
            v = None
            if node.right:
                v = self.find_next_larger(node.right)
            if node.parent and v == None:
                node = self.find_closet_larger_node(node.parent,node)
                if node:
                    return node.value
            return v
    def next_smaller(self,value):
        node = self.get_node(self.root,value)
        if node:
            v = None
            if node.left:
                v = self.find_next_smaller(node.left)
            if node.parent and v == None:
                node = self.find_closet_smaller_node(node.parent,node)
                if node:
                    return node.value
            return v
    def find_closet_larger_node(self,parent,node):
        if parent:
            if parent.value >= node.value:
                return parent
            else:
                return self.find_closet_larger_node(parent.parent,node)
    def find_closet_smaller_node(self,parent,node):
        if parent:
            if parent.value <= node.value:
                return parent
            else:
                return self.find_closet_smaller_node(parent.parent,node)
    def find_next_larger(self,node):
        if not node.left:
            return node.value
        else:
            return self.find_next_larger(node.left)
    def find_next_smaller(self,node):
        if not node.right:
            return node.value
        else:
            return self.find_next_smaller(node.right)
class BinarySearchTreeWithInternalConstraint(BinarySearchTree):
    def __init__(self,internal):
        super().__init__()
        self.internal = internal
        self.inserted = True
        self.nodesNeedSizeChange = []
        self.nodes_num_less_or_equal_toValue = 0
    def restore(self):
        self.inserted = True
        self.nodesNeedSizeChange = []
    def add_size(self):
        for i in range(len(self.nodesNeedSizeChange)):
            self.nodesNeedSizeChange[i].size += 1
    def compare_and_insert(self,root,node):
        if abs(root.value - node.value) <= self.internal:
            self.inserted = False
        if self.inserted == False:
            self.restore()
            return
        if root.value <= node.value and root.right == None:
            self.nodesNeedSizeChange.append(root)
            root.right = node
            node.parent = root
            self.add_size()
            self.restore()
        elif root.value >= node.value and root.left == None:
            self.nodesNeedSizeChange.append(root)
            root.left = node
            node.parent = root
            self.add_size()
            self.restore()
        elif root.value <= node.value:
            self.nodesNeedSizeChange.append(root)
            self.compare_and_insert(root.right,node)
        else:
            self.nodesNeedSizeChange.append(root)
            self.compare_and_insert(root.left,node)   
    def nodes_num_less_or_equal_to(self,value):
        return self.calculate_nodes_num_less_or_equal_to(self.root,value)
    def calculate_root_left_subtree_size(self,root):
        if root.left:
            size = root.left.size
        else:
            size = 0
        return size
    def calculate_nodes_num_less_or_equal_to(self,root,value):
        if root:
            if root.value == value:
                self.nodes_num_less_or_equal_toValue = self.nodes_num_less_or_equal_toValue + 1 + self.calculate_root_left_subtree_size(root)
                print("there are ",self.nodes_num_less_or_equal_toValue," nodes that happed before ",str(value))
                self.nodes_num_less_or_equal_toValue = 0
            elif value > root.value:
                self.nodes_num_less_or_equal_toValue = self.nodes_num_less_or_equal_toValue + 1 + self.calculate_root_left_subtree_size(root)
                self.calculate_nodes_num_less_or_equal_to(root.right,value)
            elif value < root.value:
                self.calculate_nodes_num_less_or_equal_to(root.left,value)
        else:
            print("0 exists")

class AVLTreeNode(BinarySearchTreeNode):
    def __init__(self,value):
        super().__init__(value)
        # self.height = 0

class AVLTree(BinarySearchTree):
    def __init__(self):
        super().__init__()
        self.sorted_list = []
    def insert(self,node):
        if not self.root:
            self.root = node
        else:
            return self.compare_and_insert(self.root,node)
    def compare_and_insert(self,root,node):
        root.size += 1
        if root.value <= node.value and root.right == None:
            root.right = node
            node.parent = root
            if not root.left and root.parent and (root.parent.right == None or root.parent.left == None):
                return (node,'right')
        elif root.value >= node.value and root.left == None:
            root.left = node
            node.parent = root
            if not root.right and root.parent and (root.parent.right == None or root.parent.left == None):
                return (node,'left')
        elif root.value <= node.value:
            return self.compare_and_insert(root.right,node)
        else:
            return self.compare_and_insert(root.left,node)
    def insert_item_to_avl_tree(self,node):
        node_dir = self.insert(node)
        if node_dir:
            self.rotate(node_dir)
    def rotate(self,node_dir):
        node,node_parent_heavy_direction = node_dir
        parent = node.parent
        grandparent = parent.parent
        if node_parent_heavy_direction == 'right':
            if grandparent.left == parent:
                self.rotate_left(node,parent,grandparent)
                self.rotate_right(node,grandparent,grandparent.parent)
            else:
                self.rotate_left(parent,grandparent,grandparent.parent)
        else:
            parent = node.parent
            grandparent = parent.parent
            if grandparent.right == parent:
                self.rotate_right(node,parent,grandparent)
                self.rotate_left(node,grandparent,grandparent.parent)
            else:
                self.rotate_right(parent,grandparent,grandparent.parent)
    def common_rotate(self,node,parent,grandparent):
        if grandparent == None:
            self.root = node
        node.parent = grandparent
        parent.parent = node
        parent.left = None 
        parent.right = None
        if grandparent:
            if grandparent.left == parent:
                grandparent.left = node
            else:
                grandparent.right = node
    def rotate_right(self,node,parent,grandparent):
        node.right = parent
        self.common_rotate(node,parent,grandparent)
    def rotate_left(self,node,parent,grandparent):
        node.left = parent
        self.common_rotate(node,parent,grandparent)
    def in_order_traverse(self,root):
        if root:
            self.in_order_traverse(root.left)
            self.sorted_list.append(root.value)
            self.in_order_traverse(root.right)

def counting_sort(arr):
    k = 100
    l = []
    for i in range(k):
        l.append([])
    for j in range(len(arr)):
        l[arr[j]].append(arr[j])
    output = []
    for i in range(k):
        output.extend(l[i])

def counting_sort_for_radix_sort(arr,exp):
    k = 625
    l = []
    for i in range(k):
        l.append([])
    for j in range(len(arr)):
        l[int(str(arr[j]//10**exp)[-1])].append(arr[j])
    output = []
    for i in range(len(arr)):
        output.extend(l[i])
    return output

def radix_sort(arr,max_num_digits):
    for i in range(max_num_digits):
        arr = counting_sort_for_radix_sort(arr,i)
    print(arr)

class LinkedListItem:
    def __init__(self,key,val):
        self.next = None
        self.prev = None
        self.key = key
        self.val = val
        self.position = None
    def get_equal_key_item_in_linked_lists(self,linked_list_item,key):
        if linked_list_item:
            if linked_list_item.key == key:
                return linked_list_item
            else:
                return linked_list_item.get_equal_key_item_in_linked_lists(linked_list_item.next,key)

class HashTable:
    def __init__(self,size):
        self.hash_table = []
        self.m = size
        self.n = 0
        from math import floor
        from random import random
        self.random_a = floor(random() * (2**64-1))
        self.random_b = floor(random() * (2**64-1))
        self.good_level = 1
        self.new_hash_table = []
    def build_hash_table(self):
        for i in range(self.m):
            self.hash_table.append(None)
    def shrink_and_grow_common_fun(self,m):
        self.m = m
        for i in range(self.m):
            self.new_hash_table.append(None)
        for linked_list_item in self.hash_table:
            self.reinsert(linked_list_item)
        self.hash_table = []
        self.hash_table.extend(self.new_hash_table)
        self.new_hash_table = []
    def shrink(self):
        self.shrink_and_grow_common_fun(self.m // 2)
    def grow(self):
        self.shrink_and_grow_common_fun(self.m * 2)
    def reinsert(self,linked_list_item):
        if linked_list_item:
            if linked_list_item.next:
                self.reinsert(linked_list_item.next)
            item = (linked_list_item.key,linked_list_item.val)
            self.insert(None,item,True)
    def get_item(self,key):
        non_integer = self.hash_function_good(key)
        linked_list_item = self.hash_table[non_integer]
        if not linked_list_item:
            return None
        else:
            linked_list_item = linked_list_item.get_equal_key_item_in_linked_lists(linked_list_item,key)
            if linked_list_item:
                return linked_list_item
    def search(self,key):
        linked_list_item = self.get_item(key)
        if linked_list_item: 
            return linked_list_item.val
        else:
            print(str(key),"not exists")
    def update(self,key,new_val):
        linked_list_item = self.get_item(key)
        if not linked_list_item:
            print(str(key),"not exists")
        else:
            linked_list_item.val = new_val
    def delete(self,key,is_reinsert=False):
        linked_list_item = self.get_item(key)
        if not linked_list_item:
            print(str(key),"not exists")
        else:
            prev_linked_list_item = linked_list_item.prev
            next_linked_list_item = linked_list_item.next
            if not prev_linked_list_item and not next_linked_list_item:
                val = linked_list_item.val
                position = linked_list_item.position
                self.hash_table[position] = None
                print("item:(",key,",",val,") has been deleted!")
                return
            if prev_linked_list_item:
                prev_linked_list_item.next = next_linked_list_item
            if next_linked_list_item:
                next_linked_list_item.prev = prev_linked_list_item
            print("item:(",key,",",linked_list_item.val,") has been deleted!")
        if not is_reinsert:
            self.n -= 1
        if self.n <= self.m/4:
            self.shrink()
    def insert(self,good_level,item,is_reinsert=False):
        if good_level == None:
            good_level = self.good_level
        key,val = item
        if self.get_item(key):
            print("key already in the hashTable and the value is : ",val)
            return
        if good_level == 0:
            non_integer = self.hash_function_bad(key)
        elif good_level == 1:
            non_integer = self.hash_function_good(key)
        else:
            non_integer = self.hash_function_theory(key)
        prior_linked_list_item = self.hash_table[non_integer]
        linked_list_item = LinkedListItem(key,val)
        linked_list_item.position = non_integer
        if is_reinsert:
            self.new_hash_table[non_integer] = linked_list_item
        else:
            self.hash_table[non_integer] = linked_list_item
        if prior_linked_list_item:
            linked_list_item.next = prior_linked_list_item
            prior_linked_list_item.prev = linked_list_item
        if not is_reinsert:
            self.n += 1
        if self.n >= self.m:
            self.grow()
    def hash_function_bad(self,key):
        return hash(key) % self.m
    def hash_function_good(self,key):
        non_integer = hash(key) % 2**64
        from math import log 
        from math import floor
        r = floor(log(self.m,2))
        v = non_integer*self.random_a%2**64
        return v >> (64-r)
    def hash_function_theory(self,key):
        non_integer = hash(key) % 2**64
        return ((self.random_a*non_integer + self.random_b) % 134567171717191) % self.m #we need a big prime number here

class RollingHash:
    ASCII_MAX_NUMBER = 98
    def __init__(self):
        self.ascii_hash_number = 0
        self.string = ""
    def ascii_hash(self,string):
        self.string = string
        n = 0
        for s in string:
            n = ord(s) + n*RollingHash.ASCII_MAX_NUMBER
        self.ascii_hash_number = n
        return n
    def append(self,c):
        self.string += c
        self.ascii_hash_number = ord(c) + self.ascii_hash_number*RollingHash.ASCII_MAX_NUMBER
    def skip(self):
        lenOfString = len(self.string)
        c = self.string[0]
        self.string = self.string[1:]
        self.ascii_hash_number = self.ascii_hash_number - ord(c)*(RollingHash.ASCII_MAX_NUMBER**(lenOfString-1))
    def item(self):
        return (self.string,self.ascii_hash_number)

def find_s_in_t(s,t):
    srh = RollingHash()
    trh = RollingHash()
    srh.ascii_hash(s)
    sInt = ""
    for i in range(len(s)):
        sInt += t[i]
    trh.ascii_hash(sInt)
    start_pos = find_s_in_t_start_position(0,srh,trh)
    if not start_pos:
        for i in range(len(s),len(t)):
            trh.append(t[i])
            trh.skip()
            start_pos = find_s_in_t_start_position(i-len(s)+1,srh,trh)
            if start_pos:
                print(start_pos)
                break
    else:
        print(start_pos)
    if start_pos != None:
        print(t[start_pos:start_pos+len(s)])

def find_s_in_t_start_position(start_pos,srh,trh):
    if srh.item() == trh.item():
        return start_pos

class OpenAddressingHashTable(HashTable):
    DELETEME = "delete me"
    def __init__(self,size):
        super().__init__(size)
        self.probing_index = 0
    def grow(self):
        if self.n >= self.m*9/10:
            super().grow()
    def hash_to_odd(self,key):
        v = hash(key)
        if v % 2 == 0:
            return v + 1
        return v
    def hash_function_good(self,key):
        hash_from_h1 = super().hash_function_good(key)
        hash_from_h2 = self.hash_to_odd(key)
        slot = (hash_from_h1 + self.probing_index*hash_from_h2) % self.m
        return slot
    def get_item(self,key):
        slot = self.hash_function_good(key)
        item = self.hash_table[slot]
        if not item:
            return None
        else:
            return (item,slot)
    def is_none(self,slot,key):
        if self.hash_table[slot] == None or self.hash_table[slot] == OpenAddressingHashTable.DELETEME:
            self.probing_index = 0
            return True
        elif self.hash_table[slot][0] == key:
            print("key already exists")
            return 'end'
        else:
            self.probing_index += 1
    def not_equal(self,item,key):
        if item:
            if item == OpenAddressingHashTable.DELETEME or item[0] != key:
                self.probing_index += 1
                return True
        self.probing_index = 0
    def search(self,key):
        item,slot = self.get_item(key) or (None,None)
        if not item:
            print(str(key),"not exists")
        if self.not_equal(item,key):
            return self.search(key)
        if item:
            return item[1]
    def reinsert(self,item):
        if item:
            self.insert(item,True)
    def delete(self,key,is_reinsert=False):
        item,slot = self.get_item(key) or (None,None)
        if not item:
            print(str(key),"not exists, so no necessary to delete it")
            return
        else:
            if self.not_equal(item,key):
                return self.delete(key)
            self.hash_table[slot] = OpenAddressingHashTable.DELETEME
            print("have deleted it")
        if not is_reinsert:
            self.n -= 1
        if self.n <= self.m/4:
            self.shrink()
    def insert(self,item,is_reinsert=False):
        slot = self.hash_function_good(item[0])
        message = self.is_none(slot,item[0])
        if message == "end":
            return
        elif message:
            self.hash_table[slot] = item
            if not is_reinsert:
                self.n += 1
            self.grow()
        else:
            self.insert(item)
    def update(self,key,new_val):
        item,slot = self.get_item(key) or (None,None)
        if not item:
            print(str(key),"not exists")
        else:
            if self.not_equal(item,key):
                return self.update(key,new_val)
            self.hash_table[slot] = (key,new_val)
def calculate_square_root(prev_val,val,precision,next_precisiton):
    #in main()
    # val = 19737661973766
    # import math
    # print("system: ",math.sqrt(val))
    # print("me: ",calculate_square_root(1,val,100000,3))
    if val < 0:
        return 
    if val == 1:
        return 1
    if len(str(prev_val)) >= precision+2:
        return float((str(prev_val)[0:precision+2]))
    else:
        t = prev_val
        a = (prev_val+val/prev_val)/2
        prev_val = float(str(a)[0:next_precisiton])
        if prev_val == t:
            return prev_val
        next_precisiton = next_precisiton*2
        return calculate_square_root(prev_val,val,precision,next_precisiton)
def multiply4(x,y,power):
    #in main()
    # print("system: ",342453243787676756342453243787676756*342453243787676756342453243787676756)
    # print("me: ",multiply4(342453243787676756342453243787676756,342453243787676756342453243787676756,128))
    if (x <= 1) or (y <= 1):
        if x == 1:
            return y
        elif y == 1:
            return x
        else:
            return 0
    else:
        power_by_2 = power >> 1
        x1 = x >> power_by_2
        x0 = x - (x1 << power_by_2)
        y1 = y >> power_by_2
        y0 = y - (y1 << power_by_2)
        z0 = multiply4(x0,y0,power_by_2)
        z2 = multiply4(x1,y1,power_by_2)
        return (z2<<power) + ((multiply4(x0,y1,power_by_2)+multiply4(x1,y0,power_by_2))<<power_by_2) + z0

def multiply3(x,y,power):
    #in main()
    # print("system: ",1444324324*184432425342)
    # print("me: ",multiply3(1444324324,184432425342,32))
    if (x <= 1) or (y <= 1):
        if x == 1:
            return y
        elif y == 1:
            return x
        else:
            return 0
    else:
        if power > 1:
            power_by_2 = power >> 1
        else:
            power_by_2 = 1
        x1 = x >> power_by_2
        x0 = x - (x1 << power_by_2)
        y1 = y >> power_by_2
        y0 = y - (y1 << power_by_2)
        z0 = multiply3(x0,y0,power_by_2)
        z2 = multiply3(x1,y1,power_by_2)
        z1 = multiply3(x0+x1,y0+y1,power_by_2) - z0 - z2
        if power_by_2 == 1:
            return (z2<<2) + (z1<<power_by_2) + z0
        return (z2<<power) + (z1<<power_by_2) + z0
    

def main():
    pass

if __name__ == "__main__":
    main()