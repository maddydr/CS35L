#!usr/bin/env/python3
import os
import sys
import zlib

class CommitNode:
    def __init__(self, commit_hash, branches=[]):
        """
        :type commit_hash: str
        """
        self.commit_hash = commit_hash
        self.parents = set()
        self.children = set()
        self.branches = branches

def topo_order_commits():
    hash_node_map, root_commits = create_dag()
    order = topo_sort(hash_node_map, root_commits)
    length = len(order)

    sticky_start = False
    for i in range(length):
        cur_commit = order[i] # get current commit 
        if (i != length-1):
            next_commit = order[i+1] # get the next commit

        if sticky_start: # if the last one was sticky, print its children
            print('=', end='')
            for c in sorted(hash_node_map[cur_commit].children):
                print(c, end=' ')
            print(' ')
            sticky_start = False # denote children have been printed

        if len(hash_node_map[cur_commit].branches) > 0:
            print(cur_commit + ' ', end='')
            for b in sorted(hash_node_map[cur_commit].branches):
                print(b, end=' ') # print branch name
            print(' ')
        else:
            print(cur_commit) # print commit alone if no branches are associated

        if (next_commit not in hash_node_map[cur_commit].parents) and (i < length - 1):
            for p in hash_node_map[cur_commit].parents:
                print(p, end=' ')
            print('=\n')
            sticky_start = True



def get_top_level():
    current_directory = os.getcwd()
    while current_directory != '/':
        path = os.path.join(current_directory, '.git') 
        if os.path.exists(path) and os.path.isdir(path):
            os.chdir(current_directory)
            break
        # else doesnt exist, go to the parent and check there
        else:
            current_directory = os.path.dirname(current_directory)
    else:
        sys.stderr.write("Not inside a Git repository\n")
        sys.exit(1)


def get_branch_names():
    # this function maps commit hashes to branch names
    get_top_level()
    path = os.path.join(os.getcwd(), '.git', 'refs', 'heads')
    os.chdir(path)
    path += '/'

    sha1_branch_map = {}
    # want to navigate to .git/refs/heads to see branches

    for root, dir, files in os.walk(path):
        for f in files:
            branch = os.path.join(root, f)
            sha1 = open(branch, 'rb').read().decode('utf-8').strip()

            if sha1 in sha1_branch_map:
                sha1_branch_map[sha1].append(branch[len(path):])
            else:
                    sha1_branch_map[sha1] = [branch[len(path):]]

    return sha1_branch_map


def create_dag():
    hash_branch = get_branch_names() # have a map of sha1 hash commits to branch names
    hash_node_map = {} 
    root_commits = [] # iniitializes empty list of root commits

    for sha1 in hash_branch: # looping through the keys of sha1 commits
        if sha1 in hash_node_map:
            hash_node_map[sha1].branches = hash_branch[sha1]
            continue
        hash_node_map[sha1] = CommitNode(sha1, hash_branch[sha1]) # create mapping instance from sha1 commit hash to a CommitNode object

        root_commits.extend(get_root_commits(hash_node_map, sha1)) # adds newly found root commits to list
    return hash_node_map, root_commits 


def get_root_commits(hash_node_map, sha1):
    root_commits = []
    node_stack = [hash_node_map[sha1]] # make a list with commits (node objects)
    get_top_level()
    path = os.path.join(os.getcwd(), '.git', 'objects')
    os.chdir(path)

    while len(node_stack) > 0: # while there are commits
        cur_node = node_stack.pop()
        sha1 = cur_node.commit_hash
        parents = set() 

        c_parent_info = zlib.decompress(open(os.getcwd() + '/' + sha1[:2] +'/' + sha1[2:], 'rb').read()).decode('utf-8').split('\n')

        for line in c_parent_info:
            if line.startswith('parent '):
                parent_sha1 = line[7:]
                parents.add(parent_sha1)
            # if line[:6] == 'parent': # if the first 6 letters of the line are parent
            #     parents.add(line[7:]) # gets the commit ID of the parent

        if len(parents) > 0:
            cur_node.parents.update(parents)
            for p in parents: # go through the parent commit hashes
                if p not in hash_node_map:
                    parent_node = CommitNode(p) # create CommitNode object of newly found parent
                    parent_node.children.add(sha1) # current sha1 is a child
                    hash_node_map[p] = parent_node # maps new parent  sha1 to the new CommitNode object
                    node_stack.append(parent_node) # add to stack, must check this one's parents to find root
                else:
                    hash_node_map[p].children.add(sha1)
        else:
            root_commits.append(sha1) # has no parent, so its a root commit
    
    return root_commits


def topo_sort(hash_node_map, root_commits):
    order = []
    visited = set()
    stack = root_commits

    while len(stack) > 0:
        top = stack[-1]
        visited.add(top) # mark as visited
        children = []
        for child in hash_node_map[top].children:
            if child not in visited:
                children.append(child) # visit neighbors until dead end, DFS
        if len(children) > 0:
            stack.append(children[0])
        else:
            order.append(stack.pop())

    return order


# I used the command strace -f python3 topo_order_commits.py [args...] 2>&1 | grep exec to verify I did not use other commands
# This command output execve("/w/home.10/cs/ugrad/reyes/CS35L/assn5/topo-ordered-commits-test-suite/venv/bin/python3", ["python3", "topo_order_commits.py", "[args...]"], 0x7ffd67e1b1a8 /* 56 vars */) = 0 
# This told me that it was launching the shell to run my script

if __name__ == '__main__':
     topo_order_commits()
