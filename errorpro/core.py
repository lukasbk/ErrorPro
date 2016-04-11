import numpy as np
from sympy import S, Expr

from errorpro.units import parse_unit
from errorpro.quantities import Quantity, get_value, get_error, get_dimension
from errorpro.dimensions.dimensions import Dimension

def assign(value, error=None, unit=None, name=None, longname=None, value_unit=None, error_unit=None, ignore_dim=False):
    """ function to create a new quantity

    Args:
     value: number or string that can be parsed by numpy, or sympy
            expression. If it's a sympy expression containing quantities, it
            will perform the calculation, otherwise it just saves the value.
     error: number that is saved as the value's uncertainty. this will replace
            any error coming from a calculation.
     unit: sympy expression of Unit objects. This is used to convert and save
           value and error in base units. Replaces value_unit and error_unit if
           specified.
     name: short name of the quantity (usually one letter). If not specified,
           quantity will get a dummy name.
     longname: optional additional description of the quantity
     value_unit: unit of value. Use this if value and error have different units.
     error_unit: unit of error.
     ignore_dim: bool. Keeps function from raising an error even if calculated
                 and given unit don't match. Then given unit is used instead.
    """

    value_formula = None
    value_factor = 1
    value_dim = Dimension()

    error_formula = None
    error_factor = 1
    error_dim = Dimension()

    # parse units
    if unit is not None:
        # if one general unit is given
        value_factor, value_dim, value_unit = parse_unit(unit)
        error_factor = value_factor
        error_dim = value_dim
        error_unit = value_unit
    else:
        # if value unit is given
        if value_unit is not None:
            value_factor, value_dim, value_unit = parse_unit(value_unit)

        # if error unit is given
        if error_unit is not None:
            error_factor, error_dim, error_unit = parse_unit(error_unit)

            # check dimension consistency between value_dim and error_dim
            if value_unit is not None and not value_dim == error_dim:
                raise RuntimeError("dimension mismatch\n%s != %s" % (value_dim, error_dim))

    # process value

    # if it's a calculation
    if isinstance(value, Expr) and not value.is_number:
        value_formula = value
        value = get_value(value_formula)

        if ignore_dim:
            # with ignore_dim=True, calculated value is converted to given unit
            value = np.float_(value_factor)*np.float_(value)
        else:
            # calculate dimension from dependency
            calculated_dim = get_dimension(value_formula)
            if value_unit is None:
                value_dim = calculated_dim
            else:
                if not calculated_dim == value_dim:
                    raise RuntimeError("dimension mismatch \n%s != %s" % (value_dim, calculated_dim))

    # if it's a number
    else:
        value=np.float_(value_factor)*np.float_(value)

    # process error
    if error is not None:
        error=np.float_(error_factor)*np.float_(error)

        # check value and error shapes and duplicate error in case
        if error.shape == () or value.shape[-len(error.shape):] == error.shape:
            error = np.resize(error, value.shape)
        else:
            raise RuntimeError("length of value and error don't match and"\
                                "can't be adjusted by duplicating.\n"\
                                "%s and %s" % (value.shape, error.shape))

    # if error can be calculated
    elif value_formula is not None:
        error, error_formula = get_error(value_formula)

        if ignore_dim:
            # with ignore_dim=True, calculated error is converted to given unit
            error = np.float_(error_factor)*np.float_(error)


    q = Quantity(name, longname)
    q.value = value
    q.value_formula = value_formula
    q.error = error
    q.error_formula = error_formula
    if value_unit is not None:
        q.prefer_unit = value_unit
    else:
        q.prefer_unit = error_unit
    if value is not None:
        q.dim = value_dim
    else:
        q.dim = error_dim

    return q
