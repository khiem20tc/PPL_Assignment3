
"""
 * @author nhphung
"""
from abc import ABC, abstractmethod, ABCMeta
from dataclasses import dataclass
from typing import List, Tuple
from AST import * 
from Visitor import *
from StaticError import *
from functools import *

class Type(ABC):
    __metaclass__ = ABCMeta
    pass
class Prim(Type):
    __metaclass__ = ABCMeta
    pass
class IntType(Prim):
    pass
class FloatType(Prim):
    pass
class StringType(Prim):
    pass
class BoolType(Prim):
    pass
class VoidType(Type):
    pass
class Unknown(Type):
    pass

@dataclass
class ArrayType(Type):
    dimen:List[int]
    eletype: Type

@dataclass
class MType:
    intype:List[Type]
    restype:Type

@dataclass
class Symbol:
    name: str
    mtype:Type

@dataclass
class Identifier_:
  def __init__(self, name, Type, Kind, param=[]):
    self.name = name
    self.type = Type
    self.kind = Kind
    self.param = param

class StaticChecker(BaseVisitor):
    def __init__(self,ast):
        self.ast = ast
        self.global_envi = [
Symbol("int_of_float",MType([FloatType()],IntType())),
Symbol("float_to_int",MType([IntType()],FloatType())),
Symbol("int_of_string",MType([StringType()],IntType())),
Symbol("string_of_int",MType([IntType()],StringType())),
Symbol("float_of_string",MType([StringType()],FloatType())),
Symbol("string_of_float",MType([FloatType()],StringType())),
Symbol("bool_of_string",MType([StringType()],BoolType())),
Symbol("string_of_bool",MType([BoolType()],StringType())),
Symbol("read",MType([],StringType())),
Symbol("print",MType([StringType()],VoidType())),
Symbol("printLn",MType([],VoidType())),
Symbol("printStr",MType([StringType()],VoidType())),
Symbol("printStrLn",MType([StringType()],VoidType()))]                           
   
    def updateType(self, name, new_type, o):
        for obj in o[0]: 
            if (name == obj.name):
                obj.type = new_type
        for obj in o[1]: 
            if (name == obj.name):
                obj.type = new_type
        
        return o
    
    def getType(self, name, o):
        #o[0] trong scope
        #o[1] ngoai scope
        #uu tien xet o[0] trong scope truoc de lay type
        for obj in o[0]: 
            if (name == obj.name):
                return obj.type 
        for obj in o[1]: 
            if (name == obj.name):
                return obj.type

    def check(self):
        return self.visit(self.ast,self.global_envi)

    def getFuncName(self, ast, o):
        if (o[0] == []):
            o[0].append( Identifier_("None", Unknown(), Function()) )
        for obj in o[0]: 
            if (ast.name.name == obj.name):
                raise Redeclared(Function(),obj.name)
        else:
            o[0].append( Identifier_(ast.name.name, Unknown(), Function() ))

        new_env = ([], o[0])

        reduce(lambda env, elem: self.visit(elem, env), ast.param, new_env)

        param = [self.getType(param.variable.name, new_env) for param in ast.param]

        func_list = []
        for x in new_env[1]:
            if type(x.kind) == Function:
                func_list.append(x)

        for i in range(len(func_list)):
            if (func_list[i].name == ast.name.name):
                func_list[i].param = param

        return func_list

    def visitProgram(self,ast,o):
        #[self.visit(x,c) for x in ast.decl]
        
        o = ([],[],[])
        var_list = []
        func_list = []
        for i in range(len(ast.decl)):
            if isinstance(ast.decl[i],VarDecl):
                self.visit(ast.decl[i],o)
                for x in o[0]:
                    if(str(x.kind) == str(Variable())):
                        var_list.append(x)
            elif isinstance(ast.decl[i],FuncDecl):
                func_list = self.getFuncName(ast.decl[i], o)

        funcDefault = []
        for x in self.global_envi:
            funcDefault.append( Identifier_(x.name, x.mtype.restype, Function(), x.mtype.intype ) )

        for x in var_list:
            funcDefault.append(x)

        for x in func_list:
            funcDefault.append(x)

        inner = []
        inner = funcDefault

        _env = (inner,[],[])

        for i in range(len(ast.decl)):
            if isinstance(ast.decl[i],FuncDecl):
                self.visit(ast.decl[i], _env)
        #reduce(lambda env,ele: self.visit(ele,env),ast.decl,_env)
        noEntryPoint = 0;
        for obj in _env[0]: 
            if (obj.name == "main" and str(obj.kind) == str(Function())):
                noEntryPoint = 1
        if (noEntryPoint == 0):
            raise NoEntryPoint()

    def visitVarDecl(self, ast, o):
        if (o[0] == []):
            o[0].append( Identifier_("None", Unknown(), Variable()) )
        for obj in o[0]: 
            if (ast.variable.name == obj.name):
                raise Redeclared(Variable(),obj.name)
        else:
            if (ast.varDimen):
                isArray = 1
                for x in ast.varDimen:
                    if type(x) != int:
                        isArray = 0
                if (isArray == 1):
                    if(ast.varInit != None):
                        o[0].append( Identifier_(ast.variable.name, ArrayType([x for x in ast.varDimen],self.visit(ast.varInit,o)[0]), Variable()) )
                    else:
                        o[0].append( Identifier_(ast.variable.name, ArrayType([x for x in ast.varDimen],Unknown()), Variable()) )
            else:
                if(ast.varInit != None):
                    o[0].append( Identifier_(ast.variable.name, self.visit(ast.varInit,o), Variable()) )
                else:
                    o[0].append( Identifier_(ast.variable.name, Unknown(), Variable()) )
        return o 

    def visitFuncDecl(self, ast, o):
        #name:str,param:List[VarDecl],local:List[Decl],stmts:List[Stmt]

        if (o[2] == []):
            o[2].append( Identifier_("None", Unknown(), Function()) )
        for obj in o[2]: 
            if (ast.name.name == obj.name):
                raise Redeclared(Function(),obj.name)
        else:
            o[2].append( Identifier_(ast.name.name, Unknown(), Function() ))

        new_outer = o[0]
        new_env = ([], new_outer, o[2])

        reduce(lambda env, elem: self.visit(elem, env), ast.param + ast.body[0] + ast.body[1], new_env)

        param = [self.getType(param.variable.name, new_env) for param in ast.param]

        # func_list = []
        # for x in new_env[1]:
        #     if type(x.kind) == Function:
        #         func_list.append(x)

        # if (func_list[-1].param == []):
        #     func_list[-1].param = param

        # for i in range(len(func_list)):
        #     if (func_list[i].name == ast.name.name):
        #         func_list[i].param = param

        for x in new_env[1]:
            if (x.name == o[2][-1].name and str(x.kind) == str(Function())):
                x.param = param
                o[2][-1].param = x.param

        for obj in o[0]: 
            if (ast.name.name == obj.name):
                for i in range(len(param)):
                    new_env[0].append( Identifier_(ast.param[i].variable.name, obj.param[i], Parameter()) )

        for obj in new_env[1]: 
            for obj_ in new_env[0]:
                if (obj_.name == obj.name):
                    continue

                if (not self.getType(obj_.name, o)) and (obj.name):
                    self.updateType(obj_.name, obj.type, o)
        return o
    
    def visitBinaryOp(self, ast, o):
        # op:str,e1:Exp,right:Exp
        left_type   = (self.visit(ast.left,o))
        right_type  = (self.visit(ast.right,o))

        # if (type(ast.left) == CallExpr):
        #     left_name = ast.left.method.name
        # elif (type(ast.left) == Id):
        #     left_name = ast.left.name
        # if (type(ast.right) == CallExpr):
        #     right_name = ast.right.method.name
        # elif (type(ast.right) == Id):
        #     right_name = ast.right.name

        if (type(ast.left) == CallExpr):
            left_name = ast.left.method.name
        elif (type(ast.left) == Id):
            left_name = ast.left.name
        elif (type(ast.left) == ArrayCell):
            if (type(ast.left.arr) == CallExpr):
                left_name = ast.left.arr.method.name
            elif (type(ast.left.arr) == Id):
                left_name = ast.left.arr.name
        if (type(ast.right) == CallExpr):
            right_name = ast.right.method.name
        elif (type(ast.right) == Id):
            right_name = ast.right.name
        elif (type(ast.right) == ArrayCell):
            if (type(ast.right.arr) == CallExpr):
                right_name = ast.right.arr.method.name
            elif (type(ast.right.arr) == Id):
                right_name = ast.right.arr.name

        if ast.op in ['+', '-', '*', '\\', '%']:
            if type(left_type) == Unknown:
                if left_name:
                    self.updateType(left_name, IntType(), o)
                    left_type = IntType()
                else:
                    raise TypeCannotBeInferred(ast.left)
            
            if type(right_type) == Unknown:
                if right_name:
                    self.updateType(right_name, IntType(), o)
                    right_type = IntType()
                else:
                    raise TypeCannotBeInferred(ast.right)

            if (type(left_type) == type(right_type)) and (type(left_type)== IntType):
                return IntType()

        elif ast.op in ['+.', '-.', '*.', '\\.']:
            if type(left_type) == Unknown:
                if left_name:
                    self.updateType(left_name, FloatType(), o)
                    left_type = FloatType()
                else:
                    raise TypeCannotBeInferred(ast.left)
            
            if type(right_type) == Unknown:
                if right_name:
                    self.updateType(right_name, FloatType(), o)
                    right_type = FloatType()
                else:
                    raise TypeCannotBeInferred(ast.right)

            if (type(left_type) == type(right_type)) and (type(left_type)== FloatType):
                return FloatType()

        elif ast.op in ['>', '<', '==', '>=', '<=', '!=']:
            if type(left_type) == Unknown:
                if left_name:
                    self.updateType(left_name, IntType(), o)
                    left_type = IntType()
                else:
                    raise TypeCannotBeInferred(ast.left)
            
            if type(right_type) == Unknown and right_name:
                if right_name:
                    self.updateType(right_name, IntType(), o)
                    right_type = IntType()
                else:
                    raise TypeCannotBeInferred(ast.right)

            if (type(left_type) == type(right_type)) and (type(left_type)== IntType):
                return BoolType()

        elif ast.op in ['>.', '=.', '<.', '=/=', '<=.', '>=.']:
            if type(left_type) == Unknown:
                if left_name:
                    self.updateType(left_name, FloatType(), o)
                    left_type = FloatType()
                else:
                    raise TypeCannotBeInferred(ast.left)
            
            if type(right_type) == Unknown:
                if right_name:
                    self.updateType(right_name, FloatType(), o)
                    right_type = FloatType()
                else:
                    raise TypeCannotBeInferred(ast.right)

            if (type(left_type) == type(right_type)) and (type(left_type)== FloatType):
                return BoolType()

        elif ast.op in ['&&', '||']:
            if type(left_type) == Unknown: 
                if left_name:
                    self.updateType(left_name, BoolType(), o)
                    left_type = BoolType()
                else:
                    raise TypeCannotBeInferred(ast.left)
            
            if type(right_type) == Unknown: 
                if right_name:
                    self.updateType(right_name, BoolType(), o)
                    right_type = BoolType()
                else:
                    raise TypeCannotBeInferred(ast.right)

            if (type(left_type) == type(right_type)) and (type(left_type)== BoolType):
                return BoolType()

        raise TypeMismatchInExpression(ast)
    
    def visitUnaryOp(self, ast, o):
        #op:str,e:Exp #op is -,-., !,i2f, floor

        param_type = self.visit(ast.body, o)
        if (type(ast.body) == CallExpr):
            name = ast.body.method.name
        elif (type(ast.body) == Id):
            name = ast.body.name
        elif (type(ast.body) == ArrayCell):
            if (type(ast.body.arr) == CallExpr):
                name = ast.body.arr.method.name
            elif (type(ast.body.arr) == Id):
                name = ast.body.arr.name

        if ast.op == '-':
            if type(param_type) == Unknown:
                if name:
                    self.updateType(name, IntType(), o)
                    return IntType()
                else:
                    raise TypeCannotBeInferred(ast.body)
            
            if type(param_type) is IntType:
                return IntType()

        elif ast.op == '-.':
            if type(param_type) == Unknown:
                if name:
                    self.updateType(name, FloatType(), o)
                    return FloatType()
                else:
                    raise TypeCannotBeInferred(ast.body)
                
            if type(param_type) is FloatType:
                return FloatType()

        elif ast.op == '!':
            if type(param_type) == Unknown:
                if name:
                    self.updateType(name, BoolType(), o)
                    return BoolType()
                else:
                    raise TypeCannotBeInferred(ast.body)

            if type(param_type) is BoolType:
                return BoolType()

        raise TypeMismatchInExpression(ast) 
    
    def visitCallExpr(self, ast, o):
        # name:str,args:List[Exp]
        isDecl = 0
        for obj in o[1]:
            if(str(obj.kind) == str(Function())):
                if ast.method.name == obj.name:
                    isDecl = 1
                    params = obj.param
        if isDecl == 0:
            raise Undeclared(Function(),ast.method.name)

        args = [self.visit(arg, o) for arg in ast.param]

        if len(params) != len(args):
            raise TypeMismatchInExpression(ast)

        for obj in o[1]:
            if(str(obj.kind) == str(Function())):
                if ast.method.name == obj.name:
                    for i in range(len(obj.param)):
                        if (type(obj.param[i]) != Unknown and type(args[i])==Unknown):
                            args[i] = obj.param[i]
                        if (type(obj.param[i]) == Unknown and type(args[i])!=Unknown):
                            obj.param[i] = args[i]
                        if (type(obj.param[i]) == Unknown or obj.type == Unknown):
                            raise TypeCannotBeInferred(ast)
                        if type(obj.param[i]) != type(args[i]):
                            raise TypeMismatchInExpression(ast)
                    else: 
                        return obj.type
        return o
    
    def visitId(self, ast, o):
        flag = 0
        for obj in o[0]: 
            if (ast.name == obj.name and ((str(obj.kind) == str(Variable()))) or (str(obj.kind) == str(Parameter()))):
                return obj.type
                flag = 1
        if (flag == 0):
            for obj in o[1]: 
                if (ast.name == obj.name and ((str(obj.kind) == str(Variable()))) or (str(obj.kind) == str(Parameter()))):
                    return obj.type
        raise Undeclared(Identifier(),ast.name)
    
    def visitArrayCell(self, ast, o):
        if (type(self.visit(ast.arr,o)) != ArrayType):
            TypeMismatchInExpression(ast)
        for x in ast.idx:
            if(type(self.visit(x,o)) != IntType):
                TypeMismatchInExpression(ast)
        if (type(self.visit(ast.arr,o)) == ArrayType):
            return(self.visit(ast.arr,o).eletype)
    
    def visitAssign(self, ast, o):
        left_type   = (self.visit(ast.lhs,o))
        right_type  = (self.visit(ast.rhs,o))

        if (type(ast.lhs) == CallExpr):
            left_name = ast.lhs.method.name
        elif (type(ast.lhs) == Id):
            left_name = ast.lhs.name
        elif (type(ast.lhs) == ArrayCell):
            if (type(ast.lhs.arr) == CallExpr):
                left_name = ast.lhs.arr.method.name
            elif (type(ast.lhs.arr) == Id):
                left_name = ast.lhs.arr.name
        if (type(ast.rhs) == CallExpr):
            right_name = ast.rhs.method.name
        elif (type(ast.rhs) == Id):
            right_name = ast.rhs.name
        elif (type(ast.rhs) == ArrayCell):
            if (type(ast.rhs.arr) == CallExpr):
                right_name = ast.rhs.arr.method.name
            elif (type(ast.rhs.arr) == Id):
                right_name = ast.rhs.arr.name

        if type(self.visit(ast.lhs,o)) == Unknown and type(self.visit(ast.rhs,o)) == Unknown:
            raise TypeCannotBeInferred(ast)
        elif type(self.visit(ast.lhs,o)) == Unknown and type(self.visit(ast.rhs,o)) != Unknown:
            flag = 0;
            for obj in o[0]: 
                if (left_name == obj.name):
                    obj.type = self.visit(ast.rhs,o)
                    left_type = self.visit(ast.rhs,o)
                    flag = 1;
            if flag == 0:        
                for obj in o[1]: 
                    if (left_name == obj.name):
                        obj.type = self.visit(ast.rhs,o)
                        left_type = self.visit(ast.rhs,o)
        elif type(self.visit(ast.rhs,o)) == Unknown and type(self.visit(ast.lhs,o)) != Unknown:
            flag = 0;
            for obj in o[0]: 
                if (right_name == obj.name):
                    obj.type = self.visit(ast.lhs,o)
                    right_type = self.visit(ast.lhs,o)
                    flag = 1;
            if flag == 0:        
                for obj in o[1]: 
                    if (right_name == obj.name):
                        obj.type = self.visit(ast.lhs,o)
                        right_type = self.visit(ast.lhs,o)
        if type(right_type) != Unknown and type(left_type) != Unknown:
            if type(left_type) != type(right_type):
                raise TypeMismatchInStatement(ast) 
            if (type(left_type) == type(right_type) and (type(left_type)) == VoidType):
                raise TypeMismatchInStatement(ast) 
        return o
    
    def visitIf(self, ast, o):
        # if type(ast.ifthenStmt[0][0]) != Id: 
        #     if type(self.visit(ast.ifthenStmt[0][0],o)) != BoolType:
        #         raise TypeMismatchInStatement(ast)
        # else:
        #     self.updateType(ast.ifthenStmt[0][0].name,BoolType(),o)
        type_cond_expr = self.visit(ast.ifthenStmt[0][0],o)
        if (type(type_cond_expr) == Unknown):
            self.updateType(ast.ifthenStmt[0][0].name,BoolType(),o)
            type_cond_expr = BoolType()
        if (type(type_cond_expr)!=BoolType):
            raise TypeMismatchInStatement(ast)
        new_outer = o[1]
        for x in o[0]:
            new_outer.append(x)
        new_envv = ([], new_outer, o[2])
        for i in range(len(ast.ifthenStmt)):
            reduce(lambda env, elem: self.visit(elem, env), ast.ifthenStmt[i][1] + ast.ifthenStmt[i][2], new_envv)
        for i in range(len(ast.elseStmt[0])):
            self.visit(ast.elseStmt[0][i],new_envv)
        for i in range(len(ast.elseStmt[1])):
            self.visit(ast.elseStmt[1][i],new_envv)
        return o
    
    def visitFor(self, ast, o):
        new_outer = o[1]
        for x in o[0]:
            new_outer.append(x)
        new_envv = ([], new_outer, o[2])
        type_idx1 = self.visit(ast.idx1,new_envv)
        type_expr1 = self.visit(ast.expr1, new_envv)
        type_expr2 = self.visit(ast.expr2, new_envv)
        type_expr3 = self.visit(ast.expr3, new_envv)
        if type(type_idx1) == Unknown:
            type_idx1 = IntType()
        if type(type_expr1) == Unknown:
            type_expr1 = IntType()
        if type(type_expr2) == Unknown:
            type_expr2 = BoolType()
        if type(type_expr3) == Unknown:
            type_expr3 = IntType()
        if not(type(type_idx1)==IntType and type(type_expr1)==IntType and type(type_expr3)==IntType and type(type_expr2)==BoolType):
            raise TypeMismatchInStatement(ast) 
        for i in range(len(ast.loop[0])):
            self.visit(ast.loop[0][i],new_envv)
        for i in range(len(ast.loop[1])):
            self.visit(ast.loop[1][i],new_envv)
        return o
    
    def visitContinue(self, ast, o):
        return o
    
    def visitBreak(self, ast, o):
        return o
    
    def visitReturn(self, ast, o):
        for x in o[1]:
            if (x.name == o[2][-1].name and str(x.kind) == str(Function())):
                o[2][-1].type = x.type
                if (ast.expr):
                    if str(type(o[2][-1].type)) == str(Unknown):
                        x.type = self.visit(ast.expr,o)
                        o[2][-1].type = self.visit(ast.expr,o)
                    else:
                        if (type(self.visit(ast.expr,o)) != type(o[2][-1].type)):
                            raise TypeMismatchInStatement(ast)
                else:
                    if str(type(o[2][-1].type)) == str(Unknown):
                        x.type = VoidType()
                        o[2][-1].type = VoidType()
                    else:
                        if (str(type(o[2][-1].type)) != str(VoidType)):
                            raise TypeMismatchInStatement(ast)
        return o
    
    def visitDowhile(self, ast, o):
        # if type(ast.exp) != Id: 
        #     if type(self.visit(ast.exp,o)) != BoolType:
        #         raise TypeMismatchInStatement(ast)
        # else:
        #     self.updateType(ast.exp.name,BoolType(),o)
        type_cond_expr = self.visit(ast.exp,o)
        if (type(type_cond_expr) == Unknown):
            self.updateType(ast.exp.name,BoolType(),o)
            type_cond_expr = BoolType()
        if (type(type_cond_expr)!=BoolType):
            raise TypeMismatchInStatement(ast)
        new_outer = o[1]
        for x in o[0]:
            new_outer.append(x)
        new_envv = ([], new_outer, o[2])
        reduce(lambda env, elem: self.visit(elem, env), ast.sl[0] + ast.sl[1], new_envv)
        return o

    def visitWhile(self, ast, o):
        if type(ast.exp) != Id: 
            if type(self.visit(ast.exp,o)) != BoolType:
                raise TypeMismatchInStatement(ast)
        else:
            self.updateType(ast.exp.name,BoolType(),o)
        new_outer = o[1]
        for x in o[0]:
            new_outer.append(x)
        new_envv = ([], new_outer, o[2])
        reduce(lambda env, elem: self.visit(elem, env), ast.sl[0] + ast.sl[1], new_envv)
        return o

    def visitCallStmt(self, ast, o):
        # name:str,args:List[Exp]
        isDecl = 0
        for obj in o[1]:
            if(str(obj.kind) == str(Function())):
                if ast.method.name == obj.name:
                    isDecl = 1
                    params = obj.param
        if isDecl == 0:
            raise Undeclared(Function(),ast.method.name)
        args = [self.visit(arg, o) for arg in ast.param]
        if len(params) != len(args):
            raise TypeMismatchInStatement(ast)

        for obj in o[1]:
            if(str(obj.kind) == str(Function())):
                if ast.method.name == obj.name:
                    for i in range(len(args)):
                        if type(obj.param[i]) == Unknown:
                            obj.param[i] = args[i]
                            if (type(obj.param[i]) == Unknown):
                                raise TypeCannotBeInferred(ast)
                        else: 
                            if type(obj.param[i]) != type(args[i]):
                                raise TypeMismatchInStatement(ast)
                    if type(obj.type) == Unknown:
                            obj.type = VoidType()
                    else:
                        if type(obj.type) != VoidType:
                            raise TypeMismatchInStatement(ast)    
        return o
    
    # Visit Literal Values => Return Type of Literal

    def visitIntLiteral(self, ast, o):
        return IntType()

    def visitFloatLiteral(self, ast, o):
        return FloatType()

    def visitBooleanLiteral(self, ast, o):
        return BoolType()

    def visitStringLiteral(self, ast, o):
        return StringType()

    def visitArrayLiteral(self, ast, o):
        return [self.visit(obj,o) for obj in ast.value]