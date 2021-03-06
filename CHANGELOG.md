# Changelog

All notable changes to the `pythonwhat` project will be documented in this file. This project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## 2.13.0

### Changed

- `test_function()` and `test_function_v2()` now use `check_function()` and `check_args()` behind the scenes.
  That way, when we make improvements to the messaging logic, all SCTs that use any of these three functions will benefit from them.
  In the future, we will deprecate `test_function()` and `test_function_v2()` as they are not explicit enough about what is being tested and how.
- `test_function('print')` and `check_function('print')` use `Ex().has_printout()` behind the scenes when appropriate.
  This makes the SCTs much more accepting for different ways of doing printouts.
- You can now use `check_finalbody()` to check the `finally` part of a `try-except` block.
- Drastically improve `has_equal_ast()` messaging.
- If you manually specify `code` argument in `has_equal_ast()`, you _have_ to specify the `incorrect_msg` because the machine-generated one will be meaningless (for now).

### Fixed

- **BIG ONE**: You can now test method calls that have subscripts in them.
  This is particularly useful for `pandas`, where you for example want to test a call `df[df.b == 'x'].a.sum()`.
  You can now do that with:

  ```python
  # Check whether the function was called:
  Ex().check_function('df.a.sum', signature = False)
  # Check whether the function was called and generated the correct result:
  Ex().check_function('df.a.sum', signature = False).has_equal_value()
  ```

  This update means that you should no longer need to use two `has_equal_ast()`'s inside a `test_correct()` to allow for two
  different ways of doing a pandas operation. If you do, please create an issue!

- Some fixes to `has_printout()` that caused it not to work in all cases.
- `check_function()` now refers to a function call in the way that the student defined it.
  When a student uses `import pandas as pd` and then has to call a function `pd.Series()`,
  `check_function()` will refer to the function with `pd.Series()` and not `pandas.Series()`.

### Removed

- `test_dict_comp()`, `test_try_except()`, `test_generator_exp()` and `test_lambda_function()` have been removed from the API.
  The couple of SCTs on DataCamp that used these functions have been converted to use the modern `check_` functions.

## 2.12.6

### Changed

- **If manually specifying `incorrect_msg` in has_equal_x: do not prepend previously generated messages. You no longer have to set `expand_msg = ""`.**

- Overall, improvement of automaticlaly generated messages:
  + Bite-size messages that are pasted together
  + More meaningful defaults that help (see `tests/test_messaging.py`)
  + Get rid of default-generated messages scattered all over the place
  + Better description of arguments
  + Better description of calls
  + Get rid of `has_key()` and `check_key()` docs, as they will be phased out
  + Improved handling of getting results, output and values from process
  + Simplify old `test_expression_x()` functions and group in one file

## 2.12.4

### Added

- You can now robustly test printouts with `Ex().has_printout(index = x)`. This function will look for the `x`'th `print()` call in the solution code, rerun that call while capturing the output, and then look for that output in the output that was generated by the student's code submission.

  ```python
  Ex().has_printout(index = 0)
  ```

  This approach is far easier and more robust than using `Ex().check_function().check_args().has_equal_value()`.


### Changed

- Improvement in messages that are generated by default when checking `*args` and `**kwargs` arguments in function calls.

### Fixed

- You can now use `test_or()` inside `test_correct()`:

  ```python
  Ex().test_correct(
      check_object(...)
      test_or(
          check_function(...),
          has_equal_ast(...)
      )
  )
  ```


## 2.12.3

### Added

- Whether or not something should be highlighted can be specified through the state now
- You can use `<other_fun>.disable_highlighting().<anohter_fun>` anywhere in the SCT chain to disable highlighting.

### Changed

- There are no more `highlight` arguments in any `pythonwhat` SCT functions.
- `Feedback` now takes a state from which it reads which part should be highlighting and whether it should be highlighted.
- Use of `StubState` to trick the system somewhat, should be refactored at some point, but works fine.
- `test_function_v2()` and `test_function()` only higlight if the `index = 1`, i.e. when the first call of a certain function is being checked. Added tests (and updated other tests) accordingly.

## 2.12.2

### Added

- In `check_args()`, you can now use `['args', 0]` and `['kwargs', 'a']` to look for matched positional star args, and matched named star args.
  The docs have been updated accordingly: https://pythonwhat.readthedocs.io/en/stable/articles/checking_function_calls.html

### Changed

- The equality checks for lists, dicts, numpy arrays, pandas dataframes and pandas series have been made faster, without compromising backwards compatibility.

### Fixed

- There was a nasty bug with signature binding when using `check_function()` for the same function when this function took only positional args. This would alleviate the need of any `signature=False` usage, once and for all!

## 2.12.1

### Added

- Reference documentation now contains examples for `set_context()` and `set_env()`.
- A `tests/test_debug.py` file has been added to easily test questions that CDs might have.

### Changed

- There was a bug in the feedback message generation for errors. It now just refers to the console.


## 2.12.0

### Added

- All new `has_()` functions are now properly documented, so there should be no reason for you to use a `test_` function other than `test_or` and `test_correct`. If you do find yourself using it (because you don't know the alternative), ping me and we'll talk!
- Added documentation on the `check_function_def()` related functions.
- `index = 0` is now a default for functions like `check_if_else()`, `check_function()` etc.
- Like there is `set_context`, there is now `set_env` to set environment variables before using something like `has_equal_value()`. These `set_` functions serve as alternatives for the `extra_env` and `context_vals` arguments that appear in many functions and that I plan to discontinue at some point.
- Added a `test_` to `check_` article, that explains how you can go from old-style to new-style SCTs. Feel free to contribute!!

### Changed

- If you experiment locally, you will now see the feedback message that the SCT chain would generate (this is explained in the README on GitHub):

```Python
from pythonwhat.local import setup_state
s = setup_state(sol_code = "x = 4", stu_code = "x = 5")
s.check_object('x').has_equal_value()
# <traceback omitted>
# pythonwhat.Test.TestFail: Check the variable `x`. Unexpected expression value: expected `4`, got `5`.
```

- The glossary is featured more prominently in the docs, as it is a good resource to see how everything fits together.

### Removed

- There is no support for `keep_objs_in_env`, as nobody is using it.