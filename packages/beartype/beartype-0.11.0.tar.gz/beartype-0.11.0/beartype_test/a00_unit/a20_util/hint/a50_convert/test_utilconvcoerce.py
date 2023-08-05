#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2014-2022 Beartype authors.
# See "LICENSE" for further details.

'''
Project-wide **PEP-agnostic type hint conversion utility unit tests.**

This submodule unit tests the public API of the private
:mod:`beartype._util.hint.convert.utilconvcoerce` submodule.
'''

# ....................{ IMPORTS                            }....................
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# WARNING: To raise human-readable test errors, avoid importing from
# package-specific submodules at module scope.
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# ....................{ TESTS ~ coercers                   }....................
def test_coerce_func_hint_root() -> None:
    '''
    Test the private
    :func:`beartype._util.hint.convert.utilconvcoerce.coerce_func_hint_root`
    coercer.
    '''

    # ..................{ IMPORTS                            }..................
    # Defer heavyweight imports.
    from beartype._util.hint.convert.utilconvcoerce import coerce_func_hint_root

    # ..................{ CALLABLES                          }..................
    def one_legion_of_wild_thoughts() -> str:
        return 'whose wandering wings'

    # ..................{ CORE                               }..................
    # Assert this coercer preserves an isinstanceable type as is.
    assert coerce_func_hint_root(
        hint=str,
        func=one_legion_of_wild_thoughts,
        pith_name='return',
        exception_prefix='',
    ) is str

    # ..................{ PEP 585                            }..................
    # Note that the PEP 585-specific logic implemented by this coercer is
    # tested by the test_coerce_hint_any() unit test below.
    # ..................{ MYPY                               }..................
    # Note that the mypy-specific logic implemented by this coercer is
    # tested by the "a00_unit.a90_decor.code.nonpep.test_codemypy" submodule.
    # ..................{ NON-PEP                            }..................
    # Note that the tuple union-specific logic implemented by this coercer is
    # tested by... something else, presumably? *sigh*


def test_coerce_hint_any() -> None:
    '''
    Test the private
    :func:`beartype._util.hint.convert.utilconvcoerce.coerce_hint_any` coercer.
    '''

    # ..................{ IMPORTS                            }..................
    # Defer heavyweight imports.
    from beartype._util.hint.convert.utilconvcoerce import coerce_hint_any
    from beartype._util.py.utilpyversion import (
        IS_PYTHON_AT_LEAST_3_10,
        IS_PYTHON_AT_LEAST_3_9,
    )

    # ..................{ CORE                               }..................
    # Assert this coercer preserves an isinstanceable type as is.
    assert coerce_hint_any(int) is int

    # ..................{ PEP 585                            }..................
    # If the active Python interpreter targets Python >= 3.9 and thus supports
    # PEP 585...
    if IS_PYTHON_AT_LEAST_3_9:
        # Arbitrary PEP 585-compliant type hint.
        hint_pep585 = list[int]

        # Assert this coercer preserves the first passed instance of a PEP
        # 585-compliant type hint as is.
        assert coerce_hint_any(hint_pep585) is hint_pep585

        # Assert this coercer returns the first passed instance of a PEP
        # 585-compliant type hint when passed a copy of that instance. PEP
        # 585-compliant type hints are *NOT* self-caching: e.g.,
        #     >>> list[int] is list[int]
        #     False
        assert coerce_hint_any(list[int]) is hint_pep585

    # ..................{ PEP 604                            }..................
    # If the active Python interpreter targets Python >= 3.10 and thus supports
    # PEP 604...
    if IS_PYTHON_AT_LEAST_3_10:
        # Arbitrary PEP 604-compliant union.
        hint_pep604 = int | str | None

        # Assert this coercer preserves the first passed instance of a PEP
        # 604-compliant union as is.
        assert coerce_hint_any(hint_pep604) is hint_pep604

        # Assert this coercer returns the first passed instance of a PEP
        # 604-compliant type hint when passed a copy of that instance. PEP
        # 604-compliant type hints are *NOT* self-caching: e.g.,
        #     >>> int | str is int | str
        #     False
        assert coerce_hint_any(int | str | None) is hint_pep604
