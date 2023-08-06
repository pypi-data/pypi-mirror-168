import functools
import inspect
import logging
from typing import Callable

logger = logging.getLogger()


def mapArgsToKwargs(function: Callable, args: tuple, kwargs: dict) -> tuple[tuple, dict]:
	"""
	assumption: valid invocation signature
	"""
	argsList: list = list(args)
	kwargsNew: dict = kwargs.copy()

	signature: inspect.Signature = inspect.signature(function)
	defaultKwargs: dict = {k: v.default for k, v in signature.parameters.items() if v.default is not inspect.Parameter.empty}
	funcArgs: list = [arg for arg, _ in signature.parameters.items()]

	for funcArg in funcArgs:
		if argsList:
			kwargsNew[funcArg] = argsList.pop(0)

	for defaultKwargKey in defaultKwargs:
		if defaultKwargKey not in kwargsNew:
			kwargsNew[defaultKwargKey] = defaultKwargs[defaultKwargKey]
	return (), kwargsNew


def enforceStrictTyping(strictFunctionDefinition: bool = True):

	def outerFunction(function: Callable):

		@functools.wraps(function)
		def innerFunction(*args, **kwargs):
			_, newKwargs = mapArgsToKwargs(function, args, kwargs)

			allChecksPassed: bool = True
			for kwarg in newKwargs:
				expectedType: type = dict(inspect.signature(function).parameters)[kwarg].annotation
				if not strictFunctionDefinition and expectedType == inspect._empty:
					continue
				receivedValue: any = newKwargs[kwarg]
				receivedType: type = type(receivedValue)
				if receivedType != expectedType:
					allChecksPassed = False
					logger.error(f'parameter {kwarg} with value {receivedValue}: expected type {expectedType}, received type {receivedType}')

			if strictFunctionDefinition:
				returnType: type = inspect.signature(function).return_annotation
				if returnType == inspect._empty:
					allChecksPassed = False
					logger.error(f'the function does not have a return type!')

			if not allChecksPassed:
				raise TypeError('not all input parameters matched type!')

			return function(*args, **kwargs)

		return innerFunction

	return outerFunction
