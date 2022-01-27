import pint
from pint.errors import UndefinedUnitError
from django.core.exceptions import ValidationError


def validate_unit_of_measure(value):
    """
    Custom validation for unit of measure
    @param: value: unit of measure
    """

    ureg = pint.UnitRegistry()
    try:
        ureg[value]
    except UndefinedUnitError:
        raise ValidationError('{} is not a valid unit of measure'.format(value))
    