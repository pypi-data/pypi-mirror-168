utils_nm
--------

This package contains utility objects like functions and classes.

The following modules can be imported:
- db_functions: functions for database operations
- orm_models: sqlalchemy orm models for logging purposes of job executions
- util_classes: useful classes
- util_functions: useful functions
- util_decorators: useful decorator functions, classes, factories

To use (with caution), simply do:

    >>> from src.utils_nm import util_functions as uf
    >>> user_input = uf.input_prompt(name='arg', choices=('a', 'b'), default='a', enum=False)
