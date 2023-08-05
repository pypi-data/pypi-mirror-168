__version__ = '1.0.4'


from typing import Union
import ast


SafeType = Union[str, int, float, complex, list, tuple, set, dict, bool, bytes, None]


def safe_eval(expression: ast.expr, /, _locals: dict[str, SafeType]) -> SafeType:
    """Recursively evaluate expressions."""

    match expression:
        # Constant
        case ast.Constant():
            if type(expression.value) not in SafeType.__args__:
                raise TypeError(f'Unsafe value type: {type(expression.value).__name__}')
            return expression.value

        # Name
        case ast.Name():
            try:
                value = _locals[expression.id]
                if type(value) not in SafeType.__args__:
                    raise TypeError(f'Unsafe value type: {type(value).__name__}')
                return value
            except KeyError:
                raise NameError(f'Name {expression.id!r} cannot be found in locals.')

        # Collections
        case ast.List():
            return list(safe_eval(e, _locals) for e in expression.elts)
        case ast.Tuple():
            return tuple(safe_eval(e, _locals) for e in expression.elts)
        case ast.Set():
            return set(safe_eval(e, _locals) for e in expression.elts)
        case ast.Dict():
            return dict({
                safe_eval(key, _locals): safe_eval(value, _locals)
                for key, value in zip(expression.keys, expression.values)
            })

        case ast.UnaryOp():
            operand = safe_eval(expression.operand, _locals)

            match expression.op:
                case ast.UAdd():
                    return +operand
                case ast.USub():
                    return -operand
                case ast.Invert():
                    return ~operand
                case ast.Not():
                    return not operand
                case _:
                    raise TypeError(f'Unsupported operator type: {type(expression.op).__name__}')

        case ast.BinOp():
            left = safe_eval(expression.left, _locals)
            right = safe_eval(expression.right, _locals)

            match expression.op:
                # Arithmetic
                case ast.Add():
                    return left + right
                case ast.Sub():
                    return left - right
                case ast.Mult():
                    return left * right
                case ast.MatMult():
                    return left @ right
                case ast.Div():
                    return left / right
                case ast.FloorDiv():
                    return left // right
                case ast.Mod():
                    return left % right
                case ast.Pow():
                    return left ** right
                    
                # Bit operations
                case ast.BitAnd():
                    return left & right
                case ast.BitOr():
                    return left | right
                case ast.BitXor():
                    return left ^ right
                case ast.LShift():
                    return left << right
                case ast.RShift():
                    return left >> right

                case _:
                    raise TypeError(f'Unsupported operator type: {type(expression.op).__name__}')

        case ast.Compare():
            left = safe_eval(expression.left, _locals)

            for op, right in zip(expression.ops, expression.comparators):
                right = safe_eval(right, _locals)

                match op:
                    # Comparison
                    case ast.Eq():
                        left = left == right
                        break
                    case ast.NotEq():
                        left = left != right
                        break
                    case ast.Gt():
                        left = left >  right
                        break
                    case ast.Lt():
                        left = left <  right
                        break
                    case ast.GtE():
                        left = left >= right
                        break
                    case ast.LtE():
                        left = left <= right
                        break

                    # Identity
                    case ast.Is():
                        left = left is right
                        break
                    case ast.IsNot():
                        left = left is not right
                        break

                    # Membership
                    case ast.In():
                        left = left in right
                        break
                    case ast.NotIn():
                        left = left not in right
                        break

                    case _:
                        raise TypeError(f'Unsupported operator type: {type(op).__name__}')

            return left

        case ast.BoolOp():
            match expression.op:
                # Logical
                case ast.And():
                    return all(safe_eval(value, _locals) for value in expression.values)
                case ast.Or():
                    return any(safe_eval(value, _locals) for value in expression.values)
                case _:
                    raise TypeError(f'Unsupported operator type: {type(expression.op).__name__}')
        case _:
            raise TypeError(f'Unsupported expression type: {type(expression).__name__}')



def sheval(expression: str, /, _locals: dict[str, SafeType] = None) -> SafeType:
    """Safely evaluate expression. Only evaluate whitelisted types."""
    tree = ast.parse(expression, mode='eval')
    
    if not isinstance(tree, ast.Expression):
        raise TypeError('Something went wrong. Expected an `ast.Expression`.')
    return safe_eval(tree.body, _locals or {})
