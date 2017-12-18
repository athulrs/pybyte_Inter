import sys
#bytecode values
HAVE_ARG = 90
LOAD_CONSTANT = 0x64
LOAD_NAME = 0x65
STORE_NAME = 0x5a
PRINT_ITEM = 0x47
PRINT_NEWLINE = 0x48
COMPARE_OP = 0x6b
BINARY_ADD = 0x17
BINARY_MULTIPLY = 0x14
BINARY_DIVIDE = 0x15
BINARY_SUBTRACT = 0x18
BINARY_MODULO = 0x16
POP_JUMP_IF_FALSE = 0x72
POP_JUMP_IF_TRUE = 0x73
JUMP_FORWARD = 0x6e
JUMP_ABSOLUTE = 0x71
SETUP_LOOP = 0x78
POP_BLOCK = 0x57
MAKE_FUNCTION = 0x84
RETURN_VALUE = 0x53
UNARY_NOT = 0xc
CALL_FUNCTION = 0x83
LOAD_FAST = 0x7c
STORE_FAST = 0x7d
LOAD_GLOBAL = 0x74
POP_TOP = 0x1

TYPE_TUPLE = 0x28
TYPE_INTEGER = 0x69
TYPE_STRING = 0x73
TYPE_CODE = 0x63
TYPE_NONE = 0x4e
TYPE_INTERN = 0x74
TYPE_SREF = 0x52
FUNCTION_START = 0x43

INT_LIMIT = 2 ** 20
stringref=[]
name_value={}

class Stack(object):
    def __init__(self):
        self.stack=[]
    def push(self,data):
        self.stack.append(data)
    def pop(self):
        return self.stack.pop()
    def top(self):
        return self.values[-1]
    def print_stack(self):
        print(self.stack)     

stak = Stack()

def execute(code_obj):
    while cur<len(code_obj.code):
        opcode = code_obj.code[cur]
        if opcode == LOAD_CONSTANT:   
            operand = get_oparg(code_obj.code,cur)
            stak.push(consts[operand])
            cur+=3

        elif opcode == STORE_NAME:  
            operand = get_oparg(code_obj.code,cur)
            n = stak.pop()
            if name_value(code_obj.names[operand]):
                name_value[code_obj.names[operand]] = n
            code_obj.names[operand] = n
            cur+=3

        elif opcode == PRINT_ITEM:   
            print(stak.pop())
            cur+=1

        elif opcode == PRINT_NEWLINE :    
            print()
            cur+=1

        elif opcode == SETUP_LOOP:
            cur+=3

        elif opcode == LOAD_NAME:      
            oparg = get_oparg(code_obj.code,cur)
            stak.push(code_obj.names[oparg])
            cur+=3

        elif opcode == JUMP_ABSOLUTE :   
            cur = functions.get_oparg(code_obj.code,cur)

        elif opcode == POP_BLOCK :
            cur+=1

        elif opcode == RETURN_VALUE:    
            return stak.pop()

        elif opcode == COMPARE_OP:    
            opname = get_oparg(code_obj.code,cur)
            op1 = stak.pop()
            op2 = stak.pop()
            stak.push(compare_func[opname](op2,op1))
            cur+=3

        elif opcode == POP_JUMP_IF_FALSE:  
            tar = get_oparg(code_obj.code,cur)
            value = stak.pop()
            if not value: 
                cur=tar
            else: 
                cur+=3

        elif opcode == POP_JUMP_IF_TRUE: 
            tar = get_oparg(code_obj.code,cur)
            value = stak.pop()
            if value:
                cur=target
            else:
                cur+=3

        elif opcode == BINARY_ADD:   
            stak.push(stak.pop() + stak.pop())
            cur+=1

        elif opcode == BINARY_MULTIPLY:  
            stak.push(stak.pop() * stak.pop())
            cur+=1

        elif opcode == BINARY_DIVIDE: 
            op1=stak.pop()
            op2=stak.pop()
            stak.push(op2 / op1)
            cur+=1

        elif opcode == BINARY_MODULO:   
            op1=stak.pop()
            op2=stak.pop()
            stak.push(op2 % op1)
            cur+=1

        elif opcode == BINARY_SUBTRACT:  
            op1=stak.pop()
            op2=stak.pop()
            stak.push(op2 - op1)
            cur+=1

        elif opcode == UNARY_NOT:    
            stak.push(not stak.pop())
            cur+=1

        elif opcode == JUMP_FORWARD:        
            tar = get_oparg(code_obj.code,cur)
            cur+= tar+3

        elif opcode == MAKE_FUNCTION:    
            operand = get_oparg(code_obj.code,cur)
            cur+=3

        elif opcode == CALL_FUNCTION:   
            argc = get_oparg(code_obj.code,cur)
            fun = stak.get_top_n(argc)
            save_local = fun.varnames[:]
            while argc:
                argc -= 1
                fun.varnames[argc] = stak.pop()
            stak.pop()
            rtrn = execute(fun)
            stak.push(rtrn)
            fun.varnames = save_local[:]
            cur+=3

        elif opcode == LOAD_FAST:   
            oparg = get_oparg(code_obj.code,cur)
            stak.push(code_obj.varnames[oparg])
            cur+=3

        elif opcode == STORE_FAST:   
            oparg = get_oparg(code_obj.code,cur)
            code_obj.varnames[oparg]=stak.pop()
            cur+=3

        elif opcode == LOAD_GLOBAL: 
            oparg = get_oparg(code_obj.code,cur)
            if name_value[code_obj.names[oparg]]:
                stak.push(name_value[code_obj.names[oparg]])
            else:
                stak.push(code_obj.names[oparg])
            cur+=3

        elif opcode == POP_TOP : 
            top=stak.pop()
            nex=stak.pop()
            stak.push(nex[top])
            cur+=1

        else:
            if opcode>=90:
                cur+=3
            else:
                cur+=1                   


def less_than(op1, op2):
    return op1 < op2

def less_equal(op1, op2):
    return op1 <= op2

def equal(op1, op2):
    return op1 == op2

def not_equal(op1, op2):
    return op1 != op2

def greater_than(op1, op2):
    return op1 > op2

def grt_equal(op1, op2):
    return op1 >= op2


compare_func = {
               0: less_than,
               1: less_equal,
               2: equal,
               3: not_equal,
               4: greater_than,
               5: grt_equal }


class code(object):
    def __init__(self,pyc_lst,cur=0):
        self.pyclst=pyc_lst
        self.cur=cur
        self.code=self.get_code()       
        self.consts = self.get_consts()
        self.names = self.get_names()
        self.varnames = self.get_varnames()
        self.name=self.get_name()

    def get_code(self):
        pyc_lst=self.pyclst
        cur=self.cur
        code=[]
        if chr(pyc_lst[cur])== TYPE_CODE and chr(pyc_lst[cur+17])== TYPE_STRING:
           self.argcount = dec(cur,pyc_lst)
           if self.argcount >= INT_LIMIT:
                self.argcount -= (2 * INT_LIMIT)
           cur+=17
           size = dec(cur,pyc_lst)
           cur+=5
           for i in range(size):
               code.append(pyc_lst[cur+i])
           cur = cur+size
        self.cur = cur
        return code   
           
    def get_consts(self):
        pyc_lst=self.pyclst
        cur=self.cur
        consts=[]
        size = dec(cur,pyc_lst)
        cur += 5
        for i in range(size):
            if chr(pyc_lst[cur]) == TYPE_INTEGER:  
                x = dec(cur,pyc_lst)
                if x >= INT_LIMIT:                    
                    x = x - (2 * INT_LIMIT)
                consts.append(x)
                cur += 5
            elif pyc_lst[cur] == TYPE_NONE: 
                consts.append(None)
                cur += 1
            elif chr(pyc_lst[cur])== TYPE_STRING or pyc_lst[cur]== TYPE_TUPLE: 
                char=chr(pyc_lst[cur])
                length = dec(cur,pyc_lst)
                cur += 5
                strng=''
                for j in range(length):
                    strng += chr(pyc_lst[cur+j])
                cur = cur+length
                if char == TYPE_STRING:
                     stringref.append(strng)
                consts.append(strng)
            elif chr(pyc_lst[cur])== TYPE_CODE :  
                code_obj=code(pyc_lst,cur)
                cur=code_obj.cur
                consts.append(code_obj)
            else:
                return
        self.cur=cur
        return consts

    def get_names(self):
        pyc_lst=self.pyclst
        cur=self.cur
        names=[]
        size = dec(cur,pyc_lst)    
        for i in range(size):
            if chr(pyc_lst[cur])== TYPE_STRING:
                char=chr(pyc_lst[cur])
                length= dec(cur,pyc_lst)
                cur+=5
                strng=''
                for j in range(length):
                    strng+=chr(pyc_lst[cur+j])
                if char== TYPE_STRING:
                     stringref.append(strng)
                     name_value[strng]=strng
                cur=cur+length
                names.append(strng)
            elif chr(pyc_lst[cur])== TYPE_INTERN:  
                x= dec(cur,pyc_lst)
                if x >= INT_LIMIT:
                    x = x - (2 * INT_LIMIT)
                names.append(x)
                cur+=5
            elif chr(pyc_lst[cur])== TYPE_SREF :  
                index= dec(cur,pyc_lst)
                names.append(stringref[index])
                cur+=5
        self.cur=cur
        return names  

    def get_varnames(self):
        pyc_lst = self.pyclst
        cur = self.cur
        var_names=[]
        size = dec(cur,pyc_lst)
        cur+=5
        for i in range(size):
            if chr(pyc_lst[cur])== TYPE_INTERN: 
                char=chr(pyc_lst[cur])
                length= dec(cur,pyc_lst)
                cur+=5
                strng=''
                for j in range(length):
                    strng+= chr(pyc_lst[cur+j])
                if char== TYPE_SREF:
                     stringref.append(strng)
                cur=cur+length
                var_names.append(strng)
        self.cur=cur
        return var_names

    def get_name(self):
        pyc_lst=self.pyclst
        cur=self.cur
        if chr(pyc_lst[cur])== TYPE_TUPLE:
                length= dec(cur,pyc_lst)
                char=chr(pyc_lst[cur])
                cur+=5
                strng=''
                for j in range(length):
                    strng+=chr(pyc_lst[cur+j])
                if char=='t':
                     stringref.append(strng)
                cur=cur+length
        elif chr(pyc_lst[cur])== TYPE_INTERN: 
                index= dec(cur,pyc_lst)
                strng=''
                for j in range(index):
                    strng+=chr(pyc_lst[cur+j])
                cur+=5
        self.cur=cur
        return strng

def start_of_code(lst, current=0):
    while (pyc_list[current] != TYPE_CODE and
            pyc_list[current+17] != TYPE_STRING):
        current += 1
    return current + 22


def dec(cur,lst):
    x=lst[cur+1]
    x|=lst[cur+2]<<8
    x|=lst[cur+3]<<16
    x|=lst[cur+4]<<24
    return x

def have_arg(opcode):
    if opcode > HAVE_ARG:
        return True
    else:
        return False

def get_oparg(lst,cur):
    l = lst[cur+1]
    m = lst[cur+2]
    return l | m << 8

def read_pyc(filename):
    lst=[]
    f=open(filename,'rb')
    f.read(8)  
    while True:
        val = f.read()
        if val:
            for byte in val:
                yield ord(byte)
        else:
            break

def pyc_list(filename):
    return list(read_pyc(filename))

def main():
    filename = sys.argv[1]
    pyc_lst = pyc_list(filename)
    code_obj = Code(pyc_lst)
    execute(code_obj)   

if __name__=='__main__':
    main()