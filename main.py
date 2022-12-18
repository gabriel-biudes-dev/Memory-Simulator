#Starting free space
holes = [[0, 9999]]

class Process:
    """Process class
    """
    def __init__(self, id, size, ranges):
        self.id = id
        self.size = size
        self.ranges = ranges

def showmenu():
    """Shows the application menu

    Returns:
        int: Choosen option
    """
    print('1)Show free space')
    print('2)Load process to memory')
    print('3)Finish process')
    print('4)Show process information')
    print('5)Exit')
    return int(input('Option: '))

def getsumholes():
    """Gets the total free space

    Returns:
        int: Free space
    """
    sum = 0
    for x in holes: sum += x[1] - x[0] + 1
    return sum

def showmemory():
    """Shows memory data
    """
    for x in holes: print(x)
    print(f'Total free space: {getsumholes()}')
    
def getranges(size):
    """Gets the ranges of memory spaces for a size

    Args:
        size (int): Process size

    Returns:
        list: List of ranges
    """
    finallist = []
    for x in holes:
        diff = x[1] - x[0] - size
        if diff >= 0:
            finallist.append([x[0], x[0] + size - 1])
            x[0] = x[0] + size
            break
    return finallist          

def dinalloc(p):
    """Dynamic allocation of memory in a non linear way

    Args:
        p (Process): Process

    Returns:
        list: List of ranges allocated to the process
    """
    global holes
    finalranges = []
    newholes = []
    size = p.size
    for x in holes:
        holesize = x[1] - x[0] + 1
        if size < holesize:
            finalranges.append([x[0], x[0] + size - 1])
            x[0] = x[0] + size
            newholes.append([x[0], x[1]])
            break
        else:
            finalranges.append(x)
            size = size - x[1] - x[0] - 1
    holes = newholes
    return finalranges

def loadprocess(plist):
    """Inserts a process in the memory

    Args:
        plist (list): Process list
    """
    id = int(input('Process ID: '))
    size = int(input('Process size: '))
    memoryranges = getranges(size)
    p = Process(id, size, memoryranges)
    if not p.ranges:
        sum = getsumholes()
        if sum >= size: p.ranges = dinalloc(p)
        else: 
            print('Process too large')
            print(f'Free space: {sum}')
            return
    plist.append(p)
    
def mergeintervals():
    """Merge free memory intervals
    """
    for x in holes:
        for y in holes:
            if x[0] == y[1] + 1:
                holes.append([y[0], x[1]])
                holes.remove(x)
                holes.remove(y)
    
def createhole(ranges):
    """Create new memory holes

    Args:
        ranges (list): List of ranges to be freed
    """
    for x in ranges: holes.append(x)
    mergeintervals()

def removeprocess(plist):
    """Removes a process from the memory

    Args:
        plist (list): Process list
    """
    id = int(input('Process ID: '))
    for x in plist:
        if x.id == id:
            createhole(x.ranges)
            plist.remove(x)

def showprocess(plist):
    """Shows the list of current process

    Args:
        plist (list): Process list
    """
    for x in plist:
        print(f'Process {x.id}:')
        print(f'Size: {x.size}')
        print(f'Memory ranges: {x.ranges}')

def main():
    """Main function
    """
    plist = []
    opt = showmenu()
    while opt != 6:
        if opt == 1: showmemory()
        if opt == 2: loadprocess(plist)
        if opt == 3: removeprocess(plist)
        if opt == 4: showprocess(plist)
        print()
        opt = showmenu()
        print()

if __name__ == '__main__': main()