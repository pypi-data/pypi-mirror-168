I find the supplied python traceback facilities quite awkward.
These functions provide convenient facilities.

*Latest release 20220918*:
caller(): return None if the frame offset is out of range.

## Function `caller(frame_index=-3)`

Return the `Frame` of the caller's caller.
Returns `None` if `frame_index` is out of range.

Useful `frame_index` values:
* `-1`: caller, this function
* `-2`: invoker, who wants to know the caller
* `-3`: the calling function of the invoker

The default `from_index` value is `-3`.

## Class `Frame(Frame, builtins.tuple)`

A `namedtuple` for stack frame contents.

## Function `frames()`

Return the current stack as a list of `Frame` objects.

## Function `stack_dump(fp=None, indent=0, Fs=None, skip=None)`

Recite current or supplied stack to `fp`, default `sys.stderr`.

Parameters:
* `fp`: the output file object, default `sys.stderr`
* `indent`: how many spaces to indent the stack lines, default `0`
* `Fs`: the stack `Frame`s to write,
  default obtained from the current stack
* `skip`: the number of `Frame`s to trim from the end of `Fs`;
  if `Fs` is `None` this defaults to `2` to trim the `Frame`s
  for the `stack_dump` function and its call to `frames()`,
  otherwise the default is `0` to use the supplied `Frame`s as is

# Release Log



*Release 20220918*:
caller(): return None if the frame offset is out of range.

*Release 20220429*:
caller: return None if the stack index is out of range.

*Release 20190812*:
stack_dump(): trim the last 2 frames from the listing by default (they are part of stack_dump's implementation).

*Release 20190101*:
* _Frame: rename .functionname to .funcname; caller: turn raw frames into Frames.
* caller(): accept optional frame_index, default -3.

*Release 20160827*:
Add stack_dump().

*Release 20150115*:
PyPI metadata fixups.

*Release 20150111*:
Tag for initial PyPI release of cs.py.stack.
