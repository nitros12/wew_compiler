import types
from .emitters import emit, Register

from .compiler_objects import Compilable, CompileException, LineReference


class Scoped(LineReference):
    def __init__(self, ast, scope: dict):
        super().__init__(ast)
        self.scope = scope
        self.offset = 0
        self.size = 0

    def lookup_variable(self, ctx: 'context', variable: str):
        return self.scope.get(variable)

    def declare_variable(self, ctx: 'context', variable):
        """Add variable to scope."""
        if variable.name in self.scope:
            raise CompileException(variable.line, f"Variable <{variable}> is already declared in the scope: "
                                   + ctx.current_scope.name)
        offset = self.offset + self.size  #self.size is current
        self.scope[variable.name] = variable
        variable.stack_offset = offset
        self.size += variable.size

    def compile(self, ctx):
        """Used to bump up esp over the stack variables declared in this scope"""
        yield emit.add(Register.esp, self.size)

class FunctionDecl(Scoped, Compilable):

    def __init__(self, ast):
        self.return_type = ast.type
        self.name = ast.name
        self.params = ast.params
        self.code = ast.stat  # this is a scope object now
        super().__init__(ast, {})
        # scope holding variables, prefill with parameters

        # we might decide to build calling conventions

    def __str__(self):
        return "<FUNCTION: <return: {0.return_type}> <name: {0.name}> <params: {1}> <code: {2}>>".format(
            self, ", ".join(map(str, self.params)), self.code
        )

    def compile(self, ctx):
        for i in self.params:
            self.declare_variable(ctx, i)
        yield from (i.compile(ctx) for i in self.code)
        yield from super().compile(ctx)

class Scope(Scoped, Compilable):

    def __init__(self, ast):
        super().__init__(ast, {})
        self.code = ast.code
        self.parent = None

    def compile(self, ctx):
        self.parent = ctx.current_function[-1]
        self.offset = self.parent.offset + self.parent.size
        # save the parent scope
        yield from (i.compile(ctx) for i in self.code)
        yield from super().compile(ctx)

    @property
    def name(self):
        return f"{self.parent.name} -> scope:{self.line}"

    def __str__(self):
        return "<SCOPE: " + ", ".join(map(str, self.code)) + ">"


class Variable(LineReference):

    def __init__(self, ast):
        super().__init__(ast)
        self.type = ast.type
        self.name = ast.name
        self.stack_offset = 0
        self.size = 1


class TypedVariable(Variable):

    size = 1
    is_lvalue = True

    def load_lvalue(self, register, ctx):
        yield emit.add(Register.epb, self.stack_offset)
        yield emit.mov(register, Register.acc)

    def __init__(self, ast):
        super().__init__(ast)

    def __str__(self):
        return f"<PARAM VARIABLE <NAME:{self.name}> <TYPE:{self.type}>>"


class DeclaredVariable(Variable, Compilable):

    def __init__(self, ast):
        super().__init__(ast)
        self.pt = ast.get("pt")
        self.ref = ast.get("ref")
        if self.ref == 'list':
            self.type = types.Pointer(self.type)
            # Wrap in a pointer for list declaration
            self.size = pt.value

    def __str__(self):
        return (f"<DECLVAR: <TYPE: {self.type}> <NAME: {self.name}> <pt: {self.pt}>>")

    def compile(self, ctx):
        ctx.current_scope.declare_variable(ctx, self)
        yield emit.sub(Register.esp, self.size)
        yield emit.mov(Register.esp, Register.acc)
        if self.ref == "ident" and self.pt is not None:
            yield from self.pt.compile(ctx)  # expression goes to acc
            yield emit.psh(Register.acc)
            yield from self.load_lvalue(Register.eee, ctx)
            yield emit.pop(Register.acc)
            yield emit.mov([Register.eee], Register.acc)
