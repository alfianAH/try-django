import pathlib
import uuid
from fractions import Fraction


def number_str_to_float(amount_str):
    """
    Take in an amount string to return float (if possible).
    
    Valid string returns:
    Float
    Boolean -> True

    Invalid string Returns
    Original String
    Boolean -> False
    
    Examples:
    1 1/2 -> 1.5, True
    32 -> 32.0, True
    Abc -> Abc, False
    """
    success = False
    number_as_float = amount_str
    try:
        number_as_float = float(sum(Fraction(s) for s in f"{amount_str}".split()))
    except:
        pass
    if isinstance(number_as_float, float):
        success = True
    return number_as_float, success


def recipe_ingredient_image_upload_handler(instance, filename):
    """Change file name of recipe ingredient

    Args:
        instance (class): 
        filename (str): file's name

    Returns:
        str: Path to file and new file name with unique name
    """
    fpath = pathlib.Path(filename)
    new_fname = str(uuid.uuid1())
    return 'recipes/{}.{}'.format(new_fname, fpath.suffix)