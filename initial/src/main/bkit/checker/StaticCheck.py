
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
Symbol("float_of_int",MType([IntType()],FloatType())),
Symbol("int_of_string",MType([StringType()],IntType())),
Symbol("string_of_int",MType([IntType()],StringType())),
Symbol("float_of_string",MType([StringType()],FloatType())),
Symbol("string_of_float",MType([FloatType()],StringType())),
Symbol("bool_of_string",MType([StringType()],BoolType())),
Symbol("string_of_bool",MType([BoolType()],StringType())),
Symbol("read",MType([],StringType())),
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

    def visitProgram(self,ast,o):
        #[self.visit(x,c) for x in ast.decl]
        funcDefault = []
        for x in self.global_envi:
            funcDefault.append( Identifier_(x.name, x.mtype.restype, Function(), x.mtype.intype ) )
        _env = (funcDefault,[])
        reduce(lambda env,ele: self.visit(ele,env),ast.decl,_env)
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
                # if type(obj.kind) == Variable:
                raise Redeclared(Variable(),obj.name)
                # elif type(obj.kind) == Parameter:
                #     raise Redeclared(Parameter(),obj.name)
        else:
            if(ast.varInit != None):
                o[0].append( Identifier_(ast.variable.name, self.visit(ast.varInit,o), Variable()) )
            else:
                o[0].append( Identifier_(ast.variable.name, Unknown(), Variable()) )
        return o 
    
    def visitFuncDecl(self, ast, o):
        #name:str,param:List[VarDecl],local:List[Decl],stmts:List[Stmt]
        if (o[0] == []):
            o[0].append( Identifier_("None", Unknown(), Function()) )
        for obj in o[0]: 
            if (ast.name.name == obj.name):
                raise Redeclared(Function(),obj.name)
        else:
            o[0].append( Identifier_(ast.name.name, Unknown(), Function() ))
        
        new_env = ([], o[0])
        reduce(lambda env, elem: self.visit(elem, env), ast.param + ast.body[0] + ast.body[1], new_env)

        param = [self.getType(param.variable.name, new_env) for param in ast.param]

        if (new_env[1][-1].param == []):
            new_env[1][-1].param = param

        for i in range(len(param)):
            new_env[0].append( Identifier_(ast.param[i].variable.name, new_env[1][-1].param[i], Parameter()) )

        # for i in range(len(param)):
        #     for obj in new_env[0]: 
        #         if (ast.param[i].variable.name == obj.name):
        #             raise Redeclared(Parameter(),obj.name)
        #         else:    
        #             new_env[0].append( Identifier_(ast.param[i].variable.name, new_env[1][-1].param[i], Parameter()) )
        
        #reduce(lambda env, elem: self.visit(elem, env), ast.param + ast.body[0] + ast.body[1], new_env)

        for obj in new_env[1]: 
            for obj_ in new_env[0]:
                if (obj_.name == obj.name):
                    continue

                if (not self.getType(obj_.name, o)) and (obj.name):
                    self.updateType(obj_.name, obj.type, o)

        #reduce(lambda env, elem: self.visit(elem, env), ast.param + ast.body[0] + ast.body[1], new_env)
        return o
    
    def visitBinaryOp(self, ast, o):
        # op:str,e1:Exp,right:Exp
        left_type   = (self.visit(ast.left,o))
        right_type  = (self.visit(ast.right,o))

        if (type(ast.left) == CallExpr):
            left_name = ast.left.method.name
        elif (type(ast.left) == Id):
            left_name = ast.left.name
        if (type(ast.right) == CallExpr):
            right_name = ast.right.method.name
        elif (type(ast.right) == Id):
            right_name = ast.right.name

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
            if type(left_right) == Unknown: 
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
        for obj in o[1][:-1]:
            if(str(obj.kind) == str(Function())):
                if ast.method.name == obj.name:
                    isDecl = 1
                    params = obj.param
        if isDecl == 0:
            raise Undeclared(obj.kind,ast.method.name)

        args = [self.visit(arg, o) for arg in ast.param]

        if len(params) != len(args):
            raise TypeMismatchInExpression(ast)

        for obj in o[1][:-1]:
            if(str(obj.kind) == str(Function())):
                if ast.method.name == obj.name:
                    for i in range(len(obj.param)):
                        if type(obj.param[i]) != type(args[i]):
                            raise TypeMismatchInExpression(ast)
                    else: 
                        return obj.type
                        # if obj.type == Unknown:
                        #     raise TypeMismatchInExpression(ast)
                    #     if type(obj.param[i]) == Unknown:
                    #         obj.param[i] = args[i]
                    #         if (type(obj.param[i]) == Unknown):
                    #             raise TypeCannotBeInferred(ast)
                    #     else: 
                    #         if type(obj.param[i]) != type(args[i]):
                    #             raise TypeMismatchInExpression(ast)
                    # if type(obj.type) == Unknown:
                    #         obj.type = VoidType
                    # else:
                    #     if type(obj.type) != VoidType:
                    #         raise TypeMismatchInExpression(ast)
        return o
    
    def visitId(self, ast, o):
        for obj in o[0]: 
            if (ast.name == obj.name):
                return obj.type
        for obj in o[1]: 
            if (ast.name == obj.name):
                return obj.type
        raise Undeclared(Identifier(),ast.name)
    
    def visitArrayCell(self, ast, o):
        return None
    
    def visitAssign(self, ast, o):
        # print(type(self.visit(ast.lhs,o)))
        # print(type(self.visit(ast.rhs,o)))
        if type(self.visit(ast.lhs,o)) == Unknown and type(self.visit(ast.rhs,o)) == Unknown:
            raise TypeCannotBeInferred(ast)
        elif type(self.visit(ast.lhs,o)) == Unknown and type(self.visit(ast.rhs,o)) != Unknown:
            #o[0][ast.lhs.name] = self.visit(ast.rhs,o)
            for obj in o[1]: 
                if (ast.lhs.name == obj.name):
                    obj.type = self.visit(ast.rhs,o)
            for obj in o[0]: 
                if (ast.lhs.name == obj.name):
                    obj.type = self.visit(ast.rhs,o)
        elif type(self.visit(ast.rhs,o)) == Unknown and type(self.visit(ast.lhs,o)) != Unknown:
            #o[0][ast.rhs.name] = self.visit(ast.lhs,o)
            for obj in o[1]: 
                if (ast.lhs.name == obj.name):
                    obj.type = self.visit(ast.lhs,o)
            for obj in o[0]: 
                if (ast.rhs.name == obj.name):
                    obj.type = self.visit(ast.lhs,o)
        if not(type(self.visit(ast.lhs,o)) == type(self.visit(ast.rhs,o))):
            raise TypeMismatchInStatement(ast) 
        if (type(self.visit(ast.lhs,o)) == type(self.visit(ast.rhs,o))) and str(type(self.visit(ast.lhs,o))) == str(VoidType()):
            raise TypeMismatchInStatement(ast) 
        return o
    
    def visitIf(self, ast, o):
        # if type(self.visit(ast.ifthenStmt[0][0],o)) == Unknown:
        #     raise TypeMismatchInStatement(ast)
        #     self.updateType(left_name, IntType(), o)
        #print(type(ast.ifthenStmt[0][0]))
        if type(ast.ifthenStmt[0][0]) != Id: 
            if type(self.visit(ast.ifthenStmt[0][0],o)) != BoolType:
                raise TypeMismatchInStatement(ast)
        else:
            #self.visit(ast.ifthenStmt[0][0],o) = BoolType()
            self.updateType(ast.ifthenStmt[0][0].name,BoolType(),o)
        return o
    
    def visitFor(self, ast, o):
        if not(type(self.visit(ast.idx1,o))==IntType and type(self.visit(ast.expr1,o))==IntType and type(self.visit(ast.expr3,o))==IntType and type(self.visit(ast.expr2,o))==BoolType):
            raise TypeMismatchInStatement(ast)
        return o
    
    def visitContinue(self, ast, o):
        return o
    
    def visitBreak(self, ast, o):
        return o
    
    def visitReturn(self, ast, o):
        # print(ast.expr)
        # print(o[1][-1].name)
        if (ast.expr):
            if str(type(o[1][-1].type)) == str(Unknown):
                o[1][-1].type = type(self.visit(ast.expr,o))
            else:
                if (type(self.visit(ast.expr,o)) != type(o[1][-1].type)):
                    raise TypeMismatchInStatement(ast)
        else:
            if str(type(o[1][-1].type)) == str(Unknown):
                o[1][-1].type = VoidType();
            else:
                if (str(type(o[1][-1].type)) != str(VoidType)):
                    raise TypeMismatchInStatement(ast)
        return o
    
    def visitDowhile(self, ast, o):
        if type(ast.exp) != Id: 
            if type(self.visit(ast.exp,o)) != BoolType:
                raise TypeMismatchInStatement(ast)
        else:
            self.updateType(ast.exp.name,BoolType(),o)
        return o

    def visitWhile(self, ast, o):
        if type(ast.exp) != Id: 
            if type(self.visit(ast.exp,o)) != BoolType:
                raise TypeMismatchInStatement(ast)
        else:
            self.updateType(ast.exp.name,BoolType(),o)
        return o

    def visitCallStmt(self, ast, o):
        # name:str,args:List[Exp]
        isDecl = 0
        for obj in o[1][:-1]:
            # print(obj.name)
            # print(obj.kind)
            if(str(obj.kind) == str(Function())):
                if ast.method.name == obj.name:
                    isDecl = 1
                    params = obj.param
        if isDecl == 0:
            raise Undeclared(obj.kind,ast.method.name)
        
        args = [self.visit(arg, o) for arg in ast.param]

        if len(params) != len(args):
            raise TypeMismatchInStatement(ast)

        for obj in o[1][:-1]:
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
                            obj.type = VoidType
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