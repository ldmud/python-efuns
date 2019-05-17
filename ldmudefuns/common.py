class BadArgument(TypeError):
    def __init__(self, fun, number, got, expected):
        """Initializes the exception.

           Arguments:
              fun:      The name of the function.
              number:   The number of the argument
              got:      The actual type,
              expected: The expected type.
        """
        TypeError.__init__(self, "Bad arg %d to %s: got '%s', expected '%s'." % (number, fun, got.__name__, expected.__name__,))

def check_arg(fun, nr, arg, typ):
    """Checks the argument's type and raises as BadArgument exception on mismatch.

       Arguments:
          fun:  The name of the function for the exception message
          nr:   The number of the argument
          arg:  The actual argument.
          type: The expected type.
    """
    if not isinstance(arg, typ):
        raise BadArgument(fun, nr, type(arg), typ)
