
from loozr_near_sdk.utils.constants import BASE_TEN, DEFAULT_TOKEN_DECIMAL


def getExpandedNotation(flt):
    str_vals = str(flt).split('e')
    if len(str_vals) > 1:
        coef = float(str_vals[0])
        exp = int(str_vals[1])
        return_val = ''
        if int(exp) > 0:
            return_val += str(coef).replace('.', '')
            return_val += ''.join(
                ['0' for _ in range(
                    0, abs(exp - len(
                        str(coef).split('.')[1])))])
        elif int(exp) < 0:
            return_val += '0.'
            return_val += ''.join(
                ['0' for _ in range(0, abs(exp) - 1)])
            return_val += str(coef).replace('.', '')
        return return_val
    else:
        return flt


def getBalanceAmount(amount) -> int:
    '''
    Converts account balance from an internal
    indivisible unit to NEAR or any value depending
    on the value passed to as an argument to `decimal`

    Parameters
    ----------
    amount: str|int
        balance amount to be converted
    decimal: int
        token decimal places

    Returns
    -------
    int
        The amount of balance
    '''
    return amount / pow(BASE_TEN, DEFAULT_TOKEN_DECIMAL)


def nearFormat(amount) -> int:
    return amount * pow(BASE_TEN, DEFAULT_TOKEN_DECIMAL)
