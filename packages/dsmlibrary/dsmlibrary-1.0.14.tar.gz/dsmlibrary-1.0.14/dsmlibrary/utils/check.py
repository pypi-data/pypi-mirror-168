from .requests import check_http_status_code

def check_lists_int(data=None, dataName="data"):
    if type(data) != list:
        raise Exception(f'expect {dataName} type `list`, but got ({type(data)})')
    _reject = []
    for i, d in enumerate(data):
        if type(d) != int:
            _reject.append({
                'data': d,
                'index': i
            })
    if _reject != []:
        raise Exception(f"expect {dataName} [<int>,<int>, ... , <int>] but got {_reject} ")

def check_type(variable, variableName, dtype, child=None):
    if type(variable) != dtype:
        raise Exception(f"Expect {variableName} type {dtype} but got {type(variable)}")
    if child is not None:
        for elm in variable:
            if type(elm) != child:
                raise Exception(f"{variableName} expect [{child}, {child}, ... {child}] but has {elm}({type(elm)})")