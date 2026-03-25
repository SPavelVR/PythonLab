
import grafcreate
import infobox

import numpy as np



errorBox = infobox.MessageError(label_err="Ошибка при компиляции графиков")
static_dots = 500

static_xy_range = [-10, 10]
static_r_range = [0, 10]
static_p_range = [0, 6*np.pi]

static_base_graf = {
    "dots": static_dots,
    "color": "black",
    "linestyle": '-',
    "linewidth": 2
}


# Компиляция массива функций
def compilegraf(code: str)->list:

    code = code.replace(' ', '')
    namespace, funcs = codeDivision(code)

    resfuncs = list()

    for func in funcs:
        res = compilefunc(func, namespace)
        if res is None:
            errorBox.appendErrorText(f"Функция {func}: Не верно задона функция")
            continue
        resfuncs.append(res)
        pass
    
    errorBox(showSuccess=False)
    return resfuncs
    pass


# деление кода на аргументы и функции
def codeDivision(code: str)->list:

    namespace = dict()
    funcs = list()

    rows = code.split("\n")

    line: str
    for i in range(len(rows)):

        line = rows[i]
        if len(line) == 0 or line[0] == '#': continue

        if len(line) <= 2 or line.count('=') != 1:
            errorBox.appendErrorText(f"Строка {i} \"{line}\": Не верно задона переменая или функция")
            continue
        
        l, r = line.split('=')

        if line[0] == '(' or (len(l) == 1 and l in "xyrp"):
            funcs.append(line)
            continue

        if not l[0].isalpha():
            errorBox.appendErrorText(f"Строка {i} \"{line}\": Строка не может начинаться на этот символ |{l[0]}|")
            continue
        

        try:
            r = eval(f"float({r})", grafcreate.namespaceNP)
            namespace[l] = r
        except:
            errorBox.appendErrorText(f"Строка {i} \"{line}\": Не верно задана переменая")
        
        pass

    return (namespace, funcs)
    pass


# Создает словарь для функции
def compilefunc(func: str, namespace: dict)->dict:

    if func[0] == '(': return compileporamfunc(func, namespace)

    proj, gr = func.split('=')
    param: str
    prange: list

    res: dict = static_base_graf.copy()
    
    res["label"] = func
    res["func"] = gr
    res["type"] = "explicit"

    if (proj == 'y' or proj == 'x') and not (hasArg(gr, proj) or hasArg(gr, 'p') or hasArg(gr, 'r')):
        param = 'x'
        prange = static_xy_range
        if proj == 'x': 
            param = 'y'
    elif (proj == 'r' or proj == 'p') and not (hasArg(gr, proj) or hasArg(gr, 'x') or hasArg(gr, 'y')):
        res["polar"] = 1
        param = 'p'
        prange = static_p_range
        if proj == 'p': 
            param = 'r'
            prange = static_r_range
    else:
        return None

    res["range"] = prange
    res["proj"] = proj
    res["param"] = param

    if not grafcreate.isWorkingFunc(gr, namespace):
        return None
    
    args = dict()

    for name, value in namespace.items():
        if hasArg(gr, name):
            args[name] = value
            pass
        pass

    res["args"] = args

    grafcreate.create_points_explicit(res)

    return res


def compileporamfunc(func: str, namespace: dict)->dict:
    
    if func.count(';') != 1 or func[-1] == ';' or func.count('=') != 1 or func[-1] == '=' or func.count(',') != 2: return None
    
    f, param = func.split(';')

    l, r = param.split('=')

    rp: list

    if len(l) == 0 or len(r) == 0 or not (l[0].isalpha() and r[0] == '[' and r[-1] == ']') : return None

    try:
        rp = eval(r, grafcreate.namespaceNP)
    except:
        return None

    if not grafcreate.isWorkingFunc(f, namespace | {l: 0}):
        return None
    
    res = static_base_graf.copy()

    res["type"] = "param"
    res["label"] = f
    res["func"] = f
    res["param"] = l
    res["range"] = rp
    
    args = dict()

    for name, value in namespace.items():
        if hasArg(f, name):
            args[name] = value
            pass
        pass

    res["args"] = args


    grafcreate.create_points_parametrs(res)

    return res


def hasArg(func: str, arg: str)->bool:

    text = func.split(arg)

    size = len(text)

    if size == 1: return False
    if size == 2 and len(text[0]) == len(text[1]) == 0: return True

    for i in range(size):

        if text[i] == '' and i == 0 and not text[i+1][0].isalpha():
            return True
        
        if text[i] == '' and i == (size - 1) and not text[i-1][-1].isalpha():
            return True
        
        if i == (size - 1): continue
        
        if not (text[i][-1].isalpha() or text[i+1][0].isalpha()):
            return True
        pass

    return False
    pass


def readGraf(filename: str)->list:
    grafs: list
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            grafs = eval(file.read())
            pass
    except:
        return None
    
    for graf in grafs:
        if graf.get("points_x",[])==[]:
            if graf["type"] == "explicit":
                grafcreate.create_points_explicit(graf)
            else:
                grafcreate.create_points_parametrs(graf)
            pass
        pass
    pass

if __name__ == "__main__":

    code: str
    with open('textgrafV30.txt', 'r', encoding='utf-8') as file:
        code = file.read()
        pass
    
    print(code)
    print()
    r = compilegraf(code)
    print(r)

    print("end")
    
    pass
