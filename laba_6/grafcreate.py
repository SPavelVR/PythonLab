import numpy as np

np.seterr(invalid='ignore')

namespaceNP = {
    'np': np,
    # константы
    'pi': np.pi,
    'e': np.e,
    # тригонометрические функции
    'sin': np.sin,
    'cos': np.cos,
    'tg': np.tan,
    'sh': np.sinh,
    'ch': np.cosh,
    'arcsin': np.arcsin,
    'arccos': np.arccos,
    'arctg': np.arctan,
    # логарифмы и экспоненты
    'exp': np.exp,
    'log10': np.log10,
    'log2': np.log2,
    'ln': np.log,
    # иные функции
    'sqrt': np.sqrt,
    'abs': np.abs,
}


def isWorkingFunc(fun_str: str, namespace: dict):
    param = {'x': np.int64(0), 'y': np.int64(0), 'p': np.int64(0), 'r': np.int64(0)}
    try:
        eval(fun_str, namespaceNP | namespace | param)
        return True
    except:
        return False
    pass



def create_points_explicit(func: dict):
    param = np.linspace(func["range"][0], func["range"][1], int(func["dots"]))
    
    fun_str = f'lambda {func["param"]}: {func["func"]}'
    f = eval(fun_str, namespaceNP | func["args"])

    proj = f(param)

    if type(proj) != np.ndarray:
        proj = np.array([proj] * len(param))

    mask = np.isfinite(proj) & (~np.isnan(proj))

    param = param[mask]
    proj = proj[mask]

    func[f"points_{func["param"]}"] = list(map(float, param))
    func[f"points_{func["proj"]}"] = list(map(float, proj))

    if func.get("polar", False):
        r = param if func["param"] == "r" else proj
        p = param if func["param"] == "p" else proj
        func[f"point_x"] = list(map(float, r * np.cos(p))) 
        func[f"point_y"] = list(map(float, r * np.sin(p))) 
    pass

def create_points_parametrs(func: dict)->tuple:

    t = np.linspace(func["range"][0], func["range"][1], int(func["dots"]))
    
    fx = f'lambda {func["param"]}: {func["func"].split(',')[0][1:]}'
    fy = f'lambda {func["param"]}: {func["func"].split(',')[1][:-1]}'

    fx = eval(fx, namespaceNP | func["args"])
    fy = eval(fy, namespaceNP | func["args"])

    x = fx(t)
    y = fy(t)

    mask = np.isfinite(x) & (~np.isnan(x)) & np.isfinite(y) & (~np.isnan(y))

    x = x[mask]
    y = y[mask]

    func[f"points_{func["param"]}"] = list(map(float, t))
    func["points_x"] = list(map(float, x))
    func["points_y"] = list(map(float, y))
    pass