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
def get_rid_of_float(float_val,float_val_dot_index):
    float_val_str = str(float_val)[:float_val_dot_index]
    for i in range(float_val_dot_index+1,float_val_dot_index+13):
        try:
            float_val_str += str(float_val)[i]
        except Exception as e:
            float_val_str += "0"
    prev_val = int(float_val_str)
    return prev_val

def is_real_float(index,val):
    if index != -1 and str(val)[index+1:] != "0":
        return True

def calculate_square_root(prev_val,val):
    # val = 267868768
    # import math
    # print("me: ",calculate_square_root(1,val))
    # print("system: ",math.sqrt(val))
    val_copy = val
    if val_copy < 0:
        return 
    if val_copy == 1:
        return 1
    prev_val_copy = prev_val
    prev_val_dot_index = str(prev_val).find(".")
    if is_real_float(prev_val_dot_index,prev_val):
        prev_val = get_rid_of_float(prev_val,prev_val_dot_index)
        val = get_rid_of_float(val,len(str(val)))
        print(val)
    newton_result = prev_val_copy + divide(a=int(val),b=int(prev_val))
    newton_result_dot_index = str(newton_result).find(".")
    if is_real_float(newton_result_dot_index,newton_result):
        newton_result = get_rid_of_float(newton_result,newton_result_dot_index)
        current_val = divide(newton_result,2000000000000)
    else:
        current_val = divide(int(newton_result),2)
    print(abs(current_val - prev_val_copy))
    if abs(current_val - prev_val_copy) < 0.00000001:
        return current_val
    return calculate_square_root(current_val,val_copy)
def multiply4(x,y,power):
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

def divide(a=1,b=1,prev_val=1,R=128):
    # print("system:",4/1111115)
    # print("me:",divide(4,1111115))
    current_val = (prev_val << 1) - ((multiply3(multiply3(prev_val,prev_val,128),b,128))>>R)
    if abs(current_val - prev_val) < 0.000000000001:
        return transform_to_float(multiply3(current_val,a,128),R)
    else:
        return divide(a,b,current_val,R)

def transform_to_float(big_number,R):
    high_position_bits = big_number >> R
    low_float_position_bits = bin(big_number - (high_position_bits<<R))[2:]
    float_val = 0
    v = 1
    for i in range(0,R):
        v = multiply3(v,5,128)
        start_point = len(low_float_position_bits) + i - R
        if start_point < 0:
            continue
        else:
            if low_float_position_bits[start_point] == "1":
                float_val += float("0."+str(0)*(i+1-len(str(v)))+str(v)) 
    return float(high_position_bits+float_val)

class UndirectedGraph:
    def __init__(self,u):
        self.vertices = [u]
        self.parent = {}
        self.level = {}
        self.path_in_one_depth_list = []
        self.topologic_order = []
    def adj(self,u,v):
        self.vertices.append(v)
        u.edges.append(v)
        v.edges.append(u)
    def add_vertex(self,v):
        self.vertices.append(v)
    def neighbers(self,v):
        return v.edges
    def topologic_sort(self):
        self.topologic_order = []
        result = self.dfs(route=True,cycle_check=True)
        if result == "a cycle existed":
            return result
        self.topologic_order.reverse()
        return self.topologic_order
    def dfs(self,route=True,cycle_check=False):
        self.parent = {}
        for v in self.vertices:
            if v not in self.parent:
                result = self.dfs_visit_from_u_to_v(v,None,route,cycle_check)
                self.topologic_order.append(v)
                if result and cycle_check:
                    return result
    def dfs_visit_from_u_to_v(self,u,v,route=True,cycle_check=False):
        self.path_in_one_depth_list.append(u)
        if u not in self.parent:
            self.parent[u] = None
        neighbers = u.edges
        if not neighbers:
            self.path_in_one_depth_list.pop()
        for next_vertex in neighbers:
            if next_vertex not in self.parent:
                self.parent[next_vertex] = u
                if next_vertex == v:
                    return self.show_path(v,route)
                path = self.dfs_visit_from_u_to_v(next_vertex,v,route,cycle_check)
                self.topologic_order.append(next_vertex)
                if path:
                    return path
            else:
                if cycle_check:
                    if next_vertex in self.path_in_one_depth_list:
                        return "a cycle existed"
            if self.path_in_one_depth_list:
                self.path_in_one_depth_list.pop()
    def bfs_visit_from_u_to_v(self,u,v,route=True):
        self.level = {u: 0}
        self.parent = {u: None}
        i = 1
        current_level = [u]
        end_search = False
        while current_level:
            next_level = []
            for vertex in current_level:
                if vertex == v:
                    end_search = True
                    break
                neighbers = self.neighbers(vertex)
                for next_level_vertex in neighbers:
                    if next_level_vertex not in self.level:
                        self.level[next_level_vertex] = i
                        self.parent[next_level_vertex] = vertex
                        next_level.append(next_level_vertex)
                i += 1
            if end_search:
                return self.show_path(v,route)
            current_level = next_level
        return "no path leading to the vertex in the graph"
    def show_path(self,v,route):
        if route:
            route_info = str(v)
            while self.parent[v]:
                route_info = str(self.parent[v]) + "->" + route_info
                v = self.parent[v]
            return route_info
        else:
            return "there is " + v + "in the graph"


class DirectedGraph(UndirectedGraph):
    def adj(self,u,v):
        u.edges.append(v)
        if u in self.vertices and v in self.vertices:
            return
        elif u in self.vertices:
            self.vertices.append(v)
        else:
            self.vertices.append(u)
class LinkedNode:
    def __init__(self,val):
        self.val = val
        self.edges = []
        self.in_edges = []
        self.out_edges = []
    def __str__(self):
        return self.val
    def __repr__(self):
        return self.val
    def __hash__(self):
        return ord((self.val))

class WeightedGraph(DirectedGraph):
    def __init__(self,u):
        super().__init__(u)
        self.predecessor = {}
        self.distance = {}
        self.edges = []
    def adj(self,u,v):
        u.edges.append(v)
        v["vertex"].in_edges.append({"vertex":u,"weight":v["weight"]})
        u.out_edges.append({"vertex":v["vertex"],"weight":v["weight"]})
        self.edges.append((u,v["vertex"],v["weight"]))
        if u in self.vertices and v["vertex"] in self.vertices:
            return
        elif u in self.vertices:
            self.vertices.append(v["vertex"])
        else:
            self.vertices.append(u)        
    def initialize(self,s,distance=None,predecessor=None):
        if distance == None and predecessor == None:
            self.predecessor = {}
            self.distance = {}
            distance = self.distance
            predecessor = self.predecessor
        import math
        for v in self.vertices:
            distance[v.key_name] = math.inf
            predecessor[v.key_name] = None
        distance[s.key_name] = 0
    def relax_edge(self,from_vertex,to_vertex,weight):
        if (self.distance[from_vertex] + weight) < self.distance[to_vertex]:
            self.distance[to_vertex] = self.distance[from_vertex] + weight
            self.predecessor[to_vertex] = from_vertex.key_name
            return to_vertex
        return False
    def from_source_to_calculate_shortest_paths_using_generic_way(self,s,v=None,init=False):
        if not init:
            self.initialize(s)
        if s == v:
            return
        for edge in s.out_edges:
            vertex = edge["vertex"]
            weight = edge["weight"]
            if self.relax_edge(s,vertex,weight):
                self.from_source_to_calculate_shortest_paths_using_generic_way(vertex,v,init=True)
    def from_source_to_calculate_shortest_paths_using_bellman_ford_way(self,s,init=False):
        if not init:
            self.initialize(s)
        for _ in range(len(self.vertices)-1):
            for edge in self.edges:
                u,v,weight = edge
                self.relax_edge(u,v,weight)
        self.check_whether_has_negative_cycle()
    def check_whether_has_negative_cycle(self):
        for edge in self.edges:
            u,v,weight = edge
            if self.relax_edge(u,v,weight):
                print("there exists a negative cycle")
                return True
    def from_source_to_calculate_shortest_paths_using_bi_dijkstra(self,s,v):
        forward_fib_heap = FibonacciHeap()
        backward_fib_heap = FibonacciHeap()
        forward_distance = {}
        forward_predecessor = {}
        backward_distance = {}
        backward_predecessor = {}
        self.initialize(s,forward_distance,forward_predecessor)
        self.initialize(v,backward_distance,backward_predecessor)
        forward_fib_heap.distance = forward_distance
        forward_fib_heap.predecessor = forward_predecessor
        backward_fib_heap.distance = backward_distance
        backward_fib_heap.predecessor = backward_predecessor
        import math
        import copy
        for u in self.vertices:
            forward_fib_heap.insert(copy.deepcopy(u))
            backward_fib_heap.insert(copy.deepcopy(u))
        while forward_fib_heap.number_of_nodes:
            forward_min_path_vertex = forward_fib_heap.delete_min()
            backward_min_path_vertex = backward_fib_heap.delete_min()
            if forward_min_path_vertex.key_name == backward_min_path_vertex.key_name:
                # find the minimum sum of common vertex in both side 
                min_sum = math.inf
                min_common_vertex = None
                for vertex in forward_distance:
                    if vertex in backward_distance:
                        if min_sum > (forward_distance[vertex] + backward_distance[vertex]):
                            min_sum = (forward_distance[vertex] + backward_distance[vertex])
                            min_common_vertex = vertex
                return (min_common_vertex,forward_distance,forward_predecessor,backward_distance,backward_predecessor)
            for u in forward_min_path_vertex.out_edges:
                u_vertex = u["vertex"]
                u_weight = u["weight"]
                u_new_key_value = forward_distance[forward_min_path_vertex.key_name] + u_weight
                forward_fib_heap.decrease_key(forward_min_path_vertex,u_vertex,u_new_key_value)
            for u in backward_min_path_vertex.in_edges:
                u_vertex = u["vertex"]
                u_weight = u["weight"]
                u_new_key_value = backward_distance[backward_min_path_vertex.key_name] + u_weight
                backward_fib_heap.decrease_key(backward_min_path_vertex,u_vertex,u_new_key_value)
    def from_source_to_calculate_shortest_paths_using_dijkstra(self,s,v=None):
        fib_heap = FibonacciHeap()
        self.initialize(s)
        fib_heap.distance = self.distance
        fib_heap.predecessor = self.predecessor
        import math
        for u in self.vertices:
            fib_heap.insert(u)
        while fib_heap.number_of_nodes:
            min_path_vertex = fib_heap.delete_min()
            if min_path_vertex == v:
                return 
            for u in min_path_vertex.out_edges:
                u_vertex = u["vertex"]
                u_weight = u["weight"]
                u_new_key_value = fib_heap.distance[min_path_vertex.key_name] + u_weight
                fib_heap.decrease_key(min_path_vertex,u_vertex,u_new_key_value)
    def from_source_to_calculate_shortest_paths_using_dfs(self,s,v):
        self.initialize(s)
        topologic_order = self.topologic_sort()
        s_index = None
        for i in range(0,len(topologic_order)):
            if topologic_order[i] == s:
                s_index = i 
            if s_index and i > s_index:
                self.calculate_shortest_path(topologic_order[i])
    def calculate_shortest_path(self,v):
        for weighted_vertex in v.in_edges:
            vertex = weighted_vertex["vertex"]
            weight = weighted_vertex["weight"]
            if self.distance[v] > (self.distance[vertex] + weight):
                self.distance[v] = self.distance[vertex] + weight
                self.predecessor[v] = vertex
    def dfs_visit_from_u_to_v(self,u,v,route=True,cycle_check=False):
        self.path_in_one_depth_list.append(u)
        if u not in self.parent:
            self.parent[u] = None
        neighbers = u.edges
        if not neighbers:
            self.path_in_one_depth_list.pop()
        for next_vertex in neighbers:
            next_weighted_vertex = next_vertex["vertex"]
            weight = next_vertex["weight"]
            if next_weighted_vertex not in self.parent:
                self.parent[next_weighted_vertex] = u
                if next_weighted_vertex == v:
                    return self.show_path(v,route)
                path = self.dfs_visit_from_u_to_v(next_weighted_vertex,v,route,cycle_check)
                self.topologic_order.append(next_weighted_vertex)
                if path:
                    return path
            else:
                if cycle_check:
                    if next_weighted_vertex in self.path_in_one_depth_list:
                        return "a cycle existed"
            if self.path_in_one_depth_list:
                self.path_in_one_depth_list.pop()

class FibonacciHeap:
    HAVE_CHANGED = False # if min node changed, be True
    def __init__(self):
        self.min_root = None # the node in the root list with the minimum key value
        self.number_of_nodes = 0 # the number of nodes being inserted
        self.bucket = {}
        self.distance = {}
        self.predecessor = {}
    def __str__(self):
        min_root = self.min_root
        s = str(min_root)
        if min_root and min_root.next:
            min_root_next = min_root.next
            while min_root_next != self.min_root:
                s = s + "->" + str(min_root_next)
                min_root_next = min_root_next.next
            s = s + "->" + str(min_root_next)
        return s
    def change_min_node(self,min_node,new_node):
        if min_node == None:
            FibonacciHeap.HAVE_CHANGED = True
            return
        min_node_next = min_node.next
        min_node_prev = min_node.prev
        # compares the new node with min node
        if self.distance[new_node.key_name] < self.distance[min_node.key_name]:
            # the new node has smaller key value, so change the min node to this new node
            new_node.next = min_node_next
            new_node.prev = min_node
            min_node.next = new_node
            min_node_next.prev = new_node
            FibonacciHeap.HAVE_CHANGED = True
        else:
            new_node.next = min_node
            new_node.prev = min_node_prev
            min_node.prev = new_node
            min_node_prev.next = new_node
            FibonacciHeap.HAVE_CHANGED = False
    def insert(self,fibonacci_node,operation="insert"):
        fibonacci_node.parent = None
        fibonacci_node.marked = False
        if operation == "insert":
            self.number_of_nodes += 1
        if not self.min_root:
            self.min_root = fibonacci_node
            return
        self.change_min_node(self.min_root,fibonacci_node)
        if FibonacciHeap.HAVE_CHANGED:
            self.min_root = fibonacci_node
    def merge_and_change_min_node(self,smaller_node,greater_node):
        greater_node.parent = smaller_node
        greater_node_next = greater_node.next
        greater_node_prev = greater_node.prev
        greater_node_prev.next = greater_node_next
        greater_node_next.prev = greater_node_prev
        self.bucket[smaller_node.rank] = None
        smaller_node.rank += 1
        if smaller_node.rank in self.bucket and self.bucket[smaller_node.rank]:
            self.put_into_bucket(smaller_node)
        else:
            self.bucket[smaller_node.rank] = smaller_node
        if not smaller_node.child:
            smaller_node.child = greater_node
            greater_node.next = greater_node
            greater_node.prev = greater_node
        else:
            self.change_min_node(smaller_node.child,greater_node)
    def merge(self,left_node,right_node):
        left_node_key_value = self.distance[left_node.key_name]
        right_node_key_value = self.distance[right_node.key_name]
        if left_node_key_value <= right_node_key_value:
            # right node will be the child of left node
            self.merge_and_change_min_node(left_node,right_node)
        else:
            # left node will be the child of right node
            self.merge_and_change_min_node(right_node,left_node)
    def delete_min(self):
        min_root = self.min_root
        self.min_root = None
        if not min_root:
            return 
        # after put all children of min root to the root list, return a node for having way to get the root list
        self.put_children_of_min_root_to_root_list(min_root) 
        if self.min_root == min_root:
            # only one node in the heap
            self.min_root = None
        else:
            self.confirm_new_min_root()
            self.consolidate()
            self.bucket = {}
        self.number_of_nodes -= 1
        return min_root
    def put_children_of_min_root_to_root_list(self,min_root):
        min_root_next = min_root.next
        min_root_prev = min_root.prev
        min_root_child = min_root.child
        if min_root_child:
            min_root_child.parent = None
            min_root_child.marked = False
            if min_root_prev != min_root:
                min_root_prev.next = min_root_child
                min_root_child.prev = min_root_prev
            # the last child of min root
            min_root_child_end = min_root_child
            min_root_child_end_next = min_root_child.next
            while min_root_child_end_next != min_root_child:
                min_root_child_end = min_root_child_end_next
                min_root_child_end.parent = None
                min_root_child_end.marked = False
                min_root_child_end_next = min_root_child_end_next.next
            if min_root_next != min_root:
                min_root_child_end.next = min_root_next
                min_root_next.prev = min_root_child_end
            self.min_root = min_root_child_end
        else:
            min_root_prev.next = min_root_next
            min_root_next.prev = min_root_prev
            self.min_root = min_root_next
    def confirm_new_min_root(self):
        start_node = self.min_root
        start_node_next = start_node.next
        while start_node_next != start_node:
            if self.distance[start_node_next.key_name] < self.distance[self.min_root.key_name]:
                self.min_root = start_node_next
            start_node_next = start_node_next.next
    def consolidate(self):
        start_node = self.min_root
        start_node_next = start_node.next
        self.put_into_bucket(start_node)
        while start_node_next != start_node:
            start_node_next = self.put_into_bucket(start_node_next)
    def put_into_bucket(self,fibonacci_node):
        start_node_next = fibonacci_node.next
        rank = fibonacci_node.rank
        if rank in self.bucket and self.bucket[rank]:
            self.merge(self.bucket[rank],fibonacci_node)
        else:
            self.bucket[rank] = fibonacci_node
        return start_node_next
    def decrease_key(self,source_vertex,fibonacci_node,new_key_value):
        parent = fibonacci_node.parent
        if self.distance[fibonacci_node.key_name] > new_key_value:
            self.predecessor[fibonacci_node.key_name] = source_vertex.key_name
            self.distance[fibonacci_node.key_name] = new_key_value
            if not parent: 
                self.cut(fibonacci_node)
        if not (parent == None or (parent and self.distance[parent.key_name] <= new_key_value)):
            # it means it is not a tree root
            self.cut(fibonacci_node)
            while parent and parent.marked:
                self.cut(parent)
                parent = parent.parent
    def cut(self,fibonacci_node):
        self.insert(fibonacci_node,"cut")
        if fibonacci_node.parent and fibonacci_node.parent.parent:
            fibonacci_node.parent.marked = True
class FibonacciNode:
    def __init__(self,key_name):
        self.key_name = key_name
        self.key_value = 0
        self.parent = None
        self.child = None
        self.next = self
        self.prev = self
        self.marked = False
        self.rank = 0
        self.edges = []
        self.in_edges = []
        self.out_edges = []
    def __str__(self):
        return self.key_name

# below is for Danamic Programming--------------------------

from random import random
import math
class Deck:
    SHAPES = ["hearts","clubs","spades","diamonds"]
    NUMBERS = ["a","2","3","4","5","6","7","8","9","10","j","q","k"]
    COUNT = 52 # number of cards of one deck
    DECK_NUMBER = 1 # number of decks
    CARDS_COUNT = COUNT * DECK_NUMBER # total number of cards
    def __init__(self):
        self.cards = []
        for s in Deck.SHAPES:
            for n in Deck.NUMBERS:
                self.cards.append((s,n))
        for _ in range(Deck.DECK_NUMBER-1):
            self.cards.extend(self.cards)
    def shuffle(self):
        new_cards = []  
        count = Deck.COUNT * Deck.DECK_NUMBER
        while count:
            random_number = math.floor(random()*count) 
            temp = self.cards[random_number]
            self.cards[random_number] = self.cards[count - 1]
            self.cards [count - 1] = temp
            new_cards.append(temp)
            count -= 1
        self.cards = new_cards
    def blackjack_sum_cards(self,first_card_index,second_card_index,from_card_index=None,to_card_index=None):
        number_of_ace = 0
        first_card_number = self.get_value_for_blackjack(first_card_index)
        second_card_number = self.get_value_for_blackjack(second_card_index)
        number_of_ace += self.add_ace_number(first_card_index)
        number_of_ace += self.add_ace_number(second_card_index)
        s = first_card_number + second_card_number
        if from_card_index:
            for i in range(from_card_index,to_card_index):
                card_number = self.get_value_for_blackjack(i)
                number_of_ace += self.add_ace_number(i)
                s += card_number
        s,number_of_ace = self.adjust_to_normal_sum_using_ace_to_be_1(s,number_of_ace)
        return s
    def get_value_for_blackjack(self,card_index):
        card = self.cards[card_index][1]
        if card == "a":
            return 11
        elif card == "j" or card == "q" or card == "k":
            return 10
        else:
            return int(card)
    def add_ace_number(self,card_index):
        card = self.cards[card_index][1]
        if card == "a":
            return 1
        return 0
    def adjust_to_normal_sum_using_ace_to_be_1(self,s,number_of_ace):
        while s > 21 and number_of_ace:
            number_of_ace -= 1
            s -= 10
        return (s,number_of_ace)
    def compare_player_dealer_in_blackjack(self,player_cards_sum,dealer_cards_sum):
        if player_cards_sum > dealer_cards_sum:
            return 1
        elif player_cards_sum < dealer_cards_sum:
            return -1
        else:
            return 0
    def __str__(self):
        s = ""
        count = 1
        for card in self.cards:
            shape,number = card
            s += " ["+shape+" "+number+"] "
            if count != 52:
                s += ","
            count += 1
        return s
class Text:
    def __init__(self,text,screen_width):
        self.text = text
        self.screen_width = screen_width
        self.words = None
    def get_words(self):
        self.words = self.text.split()
        return self.words
    def badness(self,start_word_index,stop_word_index):
        words_width = 0
        words_width += len(self.words[start_word_index])
        for i in range(start_word_index+1,stop_word_index+1):
            words_width += (1 + len(self.words[i]))
        if words_width > self.screen_width:
            return math.inf
        return ((self.screen_width - words_width) ** 3)
class Matrix:
    def __init__(self,content):
        self.content = content
        self.row = len(content)
        self.column = len(content[0])
class DP:
    @staticmethod
    def get_fibonacci_number(n):
        fib_memo = {
            1:1,
            2:1
        }
        if n <= 2:
            return fib_memo[n]
        for k in range(3,n+1):
            fib_memo[k] = fib_memo[1] + fib_memo[2]
            fib_memo[1] = fib_memo[2]
            fib_memo[2] = fib_memo[k]
        return fib_memo[n]
    @staticmethod
    def find_sp(wg,s,v=None):
        total_length_of_vertices = len(wg.vertices)
        is_v_found = False
        layer = [s]
        wg.initialize(s)
        for _ in range(total_length_of_vertices):
            temp_layer = []
            if is_v_found:
                return (wg.distance,wg.predecessor)
            for vertex in layer:
                for out_edge in vertex.out_edges:
                    if out_edge == v:
                        is_v_found = True
                    if wg.distance[out_edge["vertex"].key_name] > wg.distance[vertex.key_name] + out_edge["weight"]:
                        wg.distance[out_edge["vertex"].key_name] = wg.distance[vertex.key_name] + out_edge["weight"]
                        wg.predecessor[out_edge["vertex"].key_name] = vertex.key_name
                        temp_layer.append(out_edge["vertex"])
            layer = temp_layer
        return (wg.distance,wg.predecessor)
    @staticmethod
    def find_best_strategy_win_blackjack(deck):
        lose_one = -1
        tie = 0
        win_one = 1
        tracking_for_best_strategy = {} #record how to play blackjack when knowing the deck
        for i in range(Deck.CARDS_COUNT):
            tracking_for_best_strategy[i] = {"winning_coins":0,"hits_number":None,"remaining_cards":None}
        tracking_for_best_strategy[Deck.CARDS_COUNT] = {"winning_coins":0,"hits_number":None,"remaining_cards":None}
        remaining_cards = 0 #cards on the table
        while remaining_cards <= Deck.CARDS_COUNT: # number of subproblems
            if remaining_cards < 4:
                # at least 4 cards so this game can start
                tracking_for_best_strategy[remaining_cards]["winning_coins"] = 0
                remaining_cards += 1
                continue
            number_can_hits = remaining_cards - 4 #the number that a player can hit at most
            for n in range(number_can_hits+1): # number of choices
                player_cards_sum = deck.blackjack_sum_cards(-remaining_cards,-remaining_cards+2,-remaining_cards+4,-remaining_cards+4+n)
                if player_cards_sum > 21:
                    if (lose_one + tracking_for_best_strategy[remaining_cards-n-4]["winning_coins"]) >= tracking_for_best_strategy[remaining_cards]["winning_coins"]:
                        tracking_for_best_strategy[remaining_cards]["winning_coins"] = lose_one + tracking_for_best_strategy[remaining_cards-n-4]["winning_coins"]
                        tracking_for_best_strategy[remaining_cards]["hits_number"] = n
                        tracking_for_best_strategy[remaining_cards]["remaining_cards"] = remaining_cards - n - 4
                    remaining_cards += 1
                    break
                dealer_cards_ace_number = 0
                dealer_draw_cards_count = 0
                dealer_cards_sum = deck.blackjack_sum_cards(-remaining_cards+1,-remaining_cards+3)
                dealer_cards_ace_number += deck.add_ace_number(-remaining_cards+1)
                dealer_cards_ace_number += deck.add_ace_number(-remaining_cards+3)
                while dealer_cards_sum < 17 and (remaining_cards - 4 - n - dealer_draw_cards_count) > 0:
                    dealer_draw_cards_count += 1
                    dealer_cards_sum += deck.get_value_for_blackjack(-remaining_cards+4+n+dealer_draw_cards_count)
                    dealer_cards_ace_number += deck.add_ace_number(-remaining_cards+4+n+dealer_draw_cards_count)
                    dealer_cards_sum,dealer_cards_ace_number = deck.adjust_to_normal_sum_using_ace_to_be_1(dealer_cards_sum,dealer_cards_ace_number)
                if dealer_cards_sum > 21:
                    dealer_cards_sum = 0
                compare_result = deck.compare_player_dealer_in_blackjack(player_cards_sum,dealer_cards_sum)
                if (compare_result + tracking_for_best_strategy[remaining_cards-n-4-dealer_draw_cards_count]["winning_coins"]) >= tracking_for_best_strategy[remaining_cards]["winning_coins"]:
                    tracking_for_best_strategy[remaining_cards]["winning_coins"] = compare_result + tracking_for_best_strategy[remaining_cards-n-4-dealer_draw_cards_count]["winning_coins"]
                    tracking_for_best_strategy[remaining_cards]["hits_number"] = n
                    tracking_for_best_strategy[remaining_cards]["remaining_cards"] = remaining_cards - n - 4 - dealer_draw_cards_count
            remaining_cards += 1
        return tracking_for_best_strategy
    @staticmethod
    def text_justification(text):
        # subproblems: justify remaining text 0..n to have the minimum badness
        # guess: which word is the last word of the line 0..n
        # subproblem:
            #try every guess to solve a subproblem to have the minimum badness
        # recurrence/bottom up: solve every subproblem
        # finish: solve the subproblem when remaining text is n
        words = text.get_words()
        total_words_number = len(words)
        justify = {}
        for i in range(0,total_words_number+1):
            justify[i] = {"badness":math.inf,"start_word_index":None,"stop_word_index":None,"remaining_words_number":None}
        justify[0] = {"badness":0,"start_word_index":None,"stop_word_index":None,"remaining_words_number":None}
        for remaining_words_number in range(0,total_words_number+1):
            start_word_index = total_words_number - remaining_words_number
            for stop_word_index in range(start_word_index,total_words_number):
                badness_value = text.badness(start_word_index,stop_word_index) + justify[total_words_number-(stop_word_index+1)]["badness"]
                if badness_value < justify[remaining_words_number]["badness"]:
                    justify[remaining_words_number]["badness"] = badness_value
                    justify[remaining_words_number]["start_word_index"] = start_word_index
                    justify[remaining_words_number]["stop_word_index"] = stop_word_index
                    justify[remaining_words_number]["remaining_words_number"] = total_words_number - (stop_word_index+1)
        new_text = ""
        remaining_words_number = total_words_number
        while remaining_words_number:
            justify_info = justify[remaining_words_number]
            start_word_index = justify_info["start_word_index"]
            stop_word_index = justify_info["stop_word_index"]
            for i in range(start_word_index,stop_word_index+1):
                if i == start_word_index:
                    new_text += text.words[i]
                elif i == stop_word_index:
                    new_text += (" " + text.words[i] + "\n")
                else: 
                    new_text += (" " + text.words[i]) 
            remaining_words_number = justify_info["remaining_words_number"]
        return new_text
    @staticmethod
    def optimize_matrixes_multiplication(matrixes,i,j):
        identifier = str(i)+str(j)
        if identifier in matrixes_memo:
            return matrixes_memo[identifier]["cost"]
        if (j-i) == 1:
            i_matrix = matrixes[i]
            j_matrix = matrixes[j]
            cost = (i_matrix.row * j_matrix.column) * i_matrix.column
            matrixes_memo[identifier] = {}
            matrixes_memo[identifier]["row_column"] = (i_matrix.row,j_matrix.column)
            matrixes_memo[identifier]["left"] = None
            matrixes_memo[identifier]["right"] = None
            matrixes_memo[identifier]["cost"] = cost
            return cost
        elif (j-i) == 0:
            matrix = matrixes[i]
            matrixes_memo[identifier] = {}
            matrixes_memo[identifier]["row_column"] = (matrix.row,matrix.column)
            matrixes_memo[identifier]["left"] = None
            matrixes_memo[identifier]["right"] = None
            matrixes_memo[identifier]["cost"] = 0
            return 0
        else:
            #guess k from i to j-1
            if identifier not in matrixes_memo:
                matrixes_memo[identifier] = {}
                matrixes_memo[identifier]["row_column"] = None
                matrixes_memo[identifier]["left"] = None
                matrixes_memo[identifier]["right"] = None
                matrixes_memo[identifier]["cost"] = math.inf
            for k in range(i,j):
                left_matrix_cost = DP.optimize_matrixes_multiplication(matrixes,i,k)
                left_identifier = str(i) + str(k)
                left_row,left_column = matrixes_memo[left_identifier]["row_column"]
                righ_matrix_cost = DP.optimize_matrixes_multiplication(matrixes,k+1,j)
                right_identifier = str(k+1) + str(j)
                right_row,right_column = matrixes_memo[right_identifier]["row_column"]
                self_cost = (left_row*right_column)*left_column
                total_cost = self_cost + left_matrix_cost + righ_matrix_cost
                if total_cost < matrixes_memo[identifier]["cost"]:
                    matrixes_memo[identifier]["row_column"] = (left_row,right_column)
                    matrixes_memo[identifier]["left"] = left_identifier
                    matrixes_memo[identifier]["right"] = right_identifier
                    matrixes_memo[identifier]["cost"] = total_cost
            return total_cost
    @staticmethod
    def edit_distance(x,y,i,j):
        identifier = str(i) + str(j)
        if identifier in edit_distance_memo:
            return edit_distance_memo[identifier]["cost"]
        else:
            edit_distance_memo[identifier] = {}
            edit_distance_memo_structure_helper(identifier,None,None,None,math.inf)
        if i >= len(x) and j >= len(y):
            return 0
        elif i >= len(x):
            cost = 1 + DP.edit_distance(x,y,i,j+1)
            cost = edit_distance_memo_structure_helper(identifier,"insert",str(i)+str(j+1),y[j],cost)
        elif j >= len(y):
            cost = 1 + DP.edit_distance(x,y,i+1,j)
            cost = edit_distance_memo_structure_helper(identifier,"delete",str(i+1)+str(j),x[i],cost)
        else:
            insert_cost = 1 + DP.edit_distance(x,y,i,j+1)
            if insert_cost < edit_distance_memo[identifier]["cost"]:
                cost = edit_distance_memo_structure_helper(identifier,"insert",str(i)+str(j+1),y[j],insert_cost)
            delete_cost = 1 + DP.edit_distance(x,y,i+1,j)
            if delete_cost < edit_distance_memo[identifier]["cost"]:
                cost = edit_distance_memo_structure_helper(identifier,"delete",str(i+1)+str(j),x[i],delete_cost)
            if x[i] == y[j]:
                replace_cost = DP.edit_distance(x,y,i+1,j+1)
                if replace_cost < edit_distance_memo[identifier]["cost"]: 
                    cost = edit_distance_memo_structure_helper(identifier,"replace",str(i+1)+str(j+1),x[i],replace_cost)
        return cost
    @staticmethod
    def show_most_desire_knapsack_strategy(items,which,knapsack_size):
        if which == len(items):
            return 0
        if which not in knapsack_memo:
            knapsack_memo[which] = {}
        else:
            return knapsack_memo[which]["desire"]
        desire_when_put_in = -1
        if knapsack_size >= items[which].size:
            desire_when_put_in = items[which].desire + DP.show_most_desire_knapsack_strategy(items,which+1,knapsack_size-items[which].size)
        desire_when_abandon = DP.show_most_desire_knapsack_strategy(items,which+1,knapsack_size)
        if desire_when_abandon > desire_when_put_in:
            knapsack_memo_structure_helper(which,"abandon "+items[which].name,desire_when_abandon)
            return desire_when_abandon
        else:
            knapsack_memo_structure_helper(which,"put in "+items[which].name,desire_when_put_in)
            return desire_when_put_in
    @staticmethod
    def get_piano_notes_figures_guide(n,finger_for_this_note):
        identifier = n
        if n == len(notes) - 1:
            return 0
        if identifier not in piano_notes_figures_guide_memo:
            piano_notes_figures_guide_memo[identifier] = {}
            piano_notes_figures_guide_memo_structure_helper(identifier,None,math.inf)
        else:
            return piano_notes_figures_guide_memo[identifier]["difficulty"]
        for next_finger_for_next_note in ["1","2","3","4","5"]:
            difficulty = get_piano_notes_fingers_transistor_difficulty(notes[n],finger_for_this_note,notes[n+1],next_finger_for_next_note) + DP.get_piano_notes_figures_guide(n+1,next_finger_for_next_note)
            if difficulty < piano_notes_figures_guide_memo[identifier]["difficulty"]:
                piano_notes_figures_guide_memo_structure_helper(identifier,finger_for_this_note,difficulty)
                next_best_figure_for_next_note = next_finger_for_next_note
        if n == len(notes) - 2:
            piano_notes_figures_guide_memo[n+1] = {}
            piano_notes_figures_guide_memo_structure_helper(n+1,next_best_figure_for_next_note,0)
        return difficulty
        
         
matrixes_memo = {}
edit_distance_memo = {}
knapsack_memo = {}
piano_notes_figures_guide_memo = {}
def edit_distance_memo_structure_helper(identifier,operation,next_identifier,value,cost):
    edit_distance_memo[identifier]["operation"] = operation
    edit_distance_memo[identifier]["next"] = next_identifier
    edit_distance_memo[identifier]["value"] = value
    edit_distance_memo[identifier]["cost"] = cost
    return cost
def knapsack_memo_structure_helper(identifier,operation,desire):
    knapsack_memo[identifier]["operation"] = operation
    knapsack_memo[identifier]["desire"] = desire
def piano_notes_figures_guide_memo_structure_helper(identifier,finger_for_this_note,difficulty):
    piano_notes_figures_guide_memo[identifier]["finger_for_this_note"] = finger_for_this_note
    piano_notes_figures_guide_memo[identifier]["difficulty"] = difficulty
def get_piano_notes_fingers_transistor_difficulty(note1,finger1,note2,finger2):
    # need to do some research or play the piano to experience to finish this implementation
    return 1
notes = [".6",".7","1","2","3","4","5","6","7","1.","2.","3."]

class KnapsackItem:
    def __init__(self,name,size,desire):
        self.name = name
        self.size = size
        self.desire = desire
class Knapsack:
    def __init__(self,size):
        self.size = size
def main():
    for finger_for_this_note in ["1","2","3","4","5"]:
        DP.get_piano_notes_figures_guide(0,finger_for_this_note)
    print(piano_notes_figures_guide_memo)
if __name__ == "__main__":
    main()

