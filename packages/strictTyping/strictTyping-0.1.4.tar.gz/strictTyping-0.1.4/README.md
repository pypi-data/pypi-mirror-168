# strictTyping

Decorator to enforce the correct types for method invocation and definition.

---

The decorator will help you to validate if the input parameters have a valid type.

With enforce=True (default) it will also enforce that the function has a return type and all parameters have types defined.


## Help

Works for builtins (int, floats, str, bool), classes, Union, Optional...

Currently only supports toplevel types. Not supported are nested types like "list[str]"

Only the definition of the function results type is checked, not the actual result type.

## Installation

Install using `pip install -U strictTyping`

## Examples

```py
from strictTyping import strictTyping

# full valid function
@strictTyping()
def myFunction(argument: int) -> str:
	return str(argument)
	
myFunction(5) # succeeds
myFunction(5.0) # ValueError

# not enforcing typing
@strictTyping(enforce = False)
def myFunction(argument, argument2: float):
	return str(argument), str(argument2)
	
myFunction(5, 5.0) # succeeds
myFunction(5.0, 5) # ValueError

