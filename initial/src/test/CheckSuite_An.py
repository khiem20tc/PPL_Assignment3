import unittest
from TestUtils import TestChecker
from StaticError import *
from AST import *

class CheckSuite(unittest.TestCase):

    def test_undeclared_function1(self):
        """Simple program: main"""
        input = """
        Function: main             
        Body: 
            foo();
        EndBody.
                   """
        expect = str(Undeclared(Function(),"foo"))
        self.assertTrue(TestChecker.test(input,expect,401))

    def test_undeclared_function5(self):
        input = """
        Function: nerf
        Body:
        EndBody.
        Function: main
        Body:
            Var: x;
            nerf();
            x = int_of_string("hi");
            foo1(1);
            foo(foo1(1));
        EndBody.
        Function: foo1
        Parameter: x
        Body:
        EndBody.
                   """
        expect = str(Undeclared(Function(),"foo"))
        self.assertTrue(TestChecker.test(input,expect,405))

    def test_undeclared_function6(self):
        input = """
        Function: main
        Body:
            Var: x;
            Var: foo;
            x = foo1(1.) + 1;
            x = foo(3.) + 1;
        EndBody.
        Function: foo1
        Parameter: x
        Body:
        EndBody.
                   """
        expect = str(Undeclared(Function(),"foo"))
        self.assertTrue(TestChecker.test(input,expect,406))

    def test_undeclared_function7(self):
        input = """
        Function: main
        Parameter: foo1[2], foo2
        Body:
            Var: foo3;
            If True Then
                Var: foo4;
                foo3 = nwf() + foo4 + foo2();
            EndIf.
        EndBody.
        Function: nwf
        Body:
        EndBody.
                   """
        expect = str(Undeclared(Function(),"foo2"))
        self.assertTrue(TestChecker.test(input,expect,407))

    def test_undeclared_function8(self):
        input = """
        Function: main
        Parameter: main
        Body:
            Var: foo;
            foo = foo + main();
            Return 1;
        EndBody.
        Function: foo
        Body:
        EndBody.
                   """
        expect = str(Undeclared(Function(),"main"))
        self.assertTrue(TestChecker.test(input,expect,408))

    def test_undeclared_function9(self):
        input = """
        Function: main
        Parameter: main
        Body:
            Var: foo = 2;
            While False Do
                main(foo);
            EndWhile.
            Return 0;
        EndBody.
        Function: foo
        Body:
        EndBody.
                   """
        expect = str(Undeclared(Function(),"main"))
        self.assertTrue(TestChecker.test(input,expect,409))

    def test_undeclared_function10(self):
        input = """
        Function: main
        Parameter: x
        Body:
            f_o_o();
            main(1);
        EndBody.
        Function: f_o_o
        Body:
            main(2);
            f_o_o();
            Do
                Var: f_o_o;
                main(3);
                f_o_o();
            While True
            EndDo.
        EndBody.
                   """
        expect = str(Undeclared(Function(),"f_o_o"))
        self.assertTrue(TestChecker.test(input,expect,410))

    def test_undeclared_identifier1(self):
        input = """
        Function: foo
        Parameter: w
        Body:
            Var: t;
            Return 1;
        EndBody.
        Function: main
        Parameter: x, y, z
        Body:
            Var: t = 2;
            x = 1;
            y = -2;
            z = t;
            t = w;
        EndBody.
                   """
        expect = str(Undeclared(Identifier(),"w"))
        self.assertTrue(TestChecker.test(input,expect,411))
    
    def test_undeclared_identifier2(self):
        input = """
        Function: main
        Body:
            Var: a[2][2] = {{1,2},{3,4}}, b, c;
            main();
            main = a;
            Return 0;
        EndBody.
                   """
        expect = str(Undeclared(Identifier(),"main"))
        self.assertTrue(TestChecker.test(input,expect,412))
    
    def test_undeclared_identifier3(self):
        input = """
        Var: x, y, z;
        Function: main
        Body:
            Var: a = 1, b = 2, c = 3;
            x = a;
            y = b;
            z = c;
            a = foo;
            Return 0;
        EndBody.
        Function: foo
        Body:
            Return 0;
        EndBody.
                   """
        expect = str(Undeclared(Identifier(),"foo"))
        self.assertTrue(TestChecker.test(input,expect,413))

    def test_undeclared_identifier4(self):
        input = """
        Var: arr[100][100], x1, x2;
        Function: main
        Body:
            Var: arr = 2;
            x1 = arr;
            x2 = x1;
            If True Then
                Var: x = 2, x2 = 0.5, z = 0;
            EndIf.
            x2 = x;
            Return 0;
        EndBody.
                   """
        expect = str(Undeclared(Identifier(),"x"))
        self.assertTrue(TestChecker.test(input,expect,414))

    def test_undeclared_identifier5(self):
        input = """
        Var: a, b, c;
        Function: i
        Body:
        EndBody.
        Function: main
        Body:
            For (i = 0, i < 10, 2) Do
                Var: x = 1;
                Var: y = 2;
            EndFor.
            Return 0;
        EndBody.
                   """
        expect = str(Undeclared(Identifier(),"i"))
        self.assertTrue(TestChecker.test(input,expect,415))

    def test_redeclared_variable1(self):
        input = """
        Var: a = 2, a;
        Function: main
        Body:
        EndBody.
                   """
        expect = str(Redeclared(Variable(),"a"))
        self.assertTrue(TestChecker.test(input,expect,416))

    def test_redeclared_variable2(self):
        input = """
        Var: a, b, c, d;
        Var: arr[10], abc, arr = 1.;
        Function: main
        Body:
        EndBody.
                   """
        expect = str(Redeclared(Variable(),"arr"))
        self.assertTrue(TestChecker.test(input,expect,417))
    
    def test_redeclared_variable3(self):
        input = """
        Var: a;
        Var: b = 2.3;
        Var: c[2] = {1,2};
        Var: y[10][100];
        Var: read;
        Function: main
        Body:
        EndBody.
                   """
        expect = str(Redeclared(Variable(),"read"))
        self.assertTrue(TestChecker.test(input,expect,418))

    def test_redeclared_variable4(self):
        input = """
        Var: a, b, c, d;
        Function: main
        Body:
            Var: a, b, c, d;
            Var: d = 2;
        EndBody.
                   """
        expect = str(Redeclared(Variable(),"d"))
        self.assertTrue(TestChecker.test(input,expect,419))

    def test_redeclared_variable5(self):
        input = """
        Var: a, b, c, d;
        Function: main
        Parameter: a, b, c
        Body:
            Var: x, y, z;
            Var: a;
        EndBody.
                   """
        expect = str(Redeclared(Variable(),"a"))
        self.assertTrue(TestChecker.test(input,expect,420))

    def test_redeclared_parameter1(self):
        input = """
        Function: main
        Parameter: a1, a2, a1
        Body:
        EndBody.
                   """
        expect = str(Redeclared(Parameter(),"a1"))
        self.assertTrue(TestChecker.test(input,expect,421))

    def test_redeclared_parameter2(self):
        input = """
        Var: p1, p2, p3;
        Function: main
        Parameter: p1, p2, p3
        Body:
        EndBody.
        Function: foo
        Parameter: p1, p1[10], p[2][3][4]
        Body:
        EndBody.
                   """
        expect = str(Redeclared(Parameter(),"p1"))
        self.assertTrue(TestChecker.test(input,expect,422))

    def test_redeclared_parameter3(self):
        input = """
        Var: p1, p2, p3;
        Function: main
        Parameter: main
        Body:
        EndBody.
        Function: foo
        Parameter: main, foo, p1, p1
        Body:
        EndBody.
                   """
        expect = str(Redeclared(Parameter(),"p1"))
        self.assertTrue(TestChecker.test(input,expect,423))

    def test_redeclared_parameter4(self):
        input = """
        Function: main
        Parameter: main[10], main1[10], main[11][22][33]
        Body:
        EndBody.
                   """
        expect = str(Redeclared(Parameter(),"main"))
        self.assertTrue(TestChecker.test(input,expect,424))
    
    def test_redeclared_parameter5(self):
        input = """
        Function: main
        Parameter: m
        Body:
            Var: main = 9;
            Var: m = 6.5;
        EndBody.
                   """
        expect = str(Redeclared(Variable(),"m"))
        self.assertTrue(TestChecker.test(input,expect,425))

    def test_redeclared_function1(self):
        input = """
        Function: main
        Parameter: m
        Body:
        EndBody.
        Function: main
        Body:
        EndBody.
                   """
        expect = str(Redeclared(Function(),"main"))
        self.assertTrue(TestChecker.test(input,expect,426))

    def test_redeclared_function2(self):
        input = """
        Var: foo[123][1];
        Function: main
        Parameter: m
        Body:
        EndBody.
        Function: foo
        Parameter: foo
        Body:
        EndBody.
                   """
        expect = str(Redeclared(Function(),"foo"))
        self.assertTrue(TestChecker.test(input,expect,427))
    
    def test_redeclared_function3(self):
        input = """
        Var: main;
        Function: main
        Body:
        EndBody.
                   """
        expect = str(Redeclared(Function(),"main"))
        self.assertTrue(TestChecker.test(input,expect,428))

    def test_redeclared_function4(self):
        input = """
        Function: main
        Body:
            Var: foo = 2;
            Var: x = 4;
        EndBody.
        Function: foo
        Parameter: main
        Body:
        EndBody.
        Function: read
        Body:
        EndBody.
                   """
        expect = str(Redeclared(Function(),"read"))
        self.assertTrue(TestChecker.test(input,expect,429))

    def test_redeclared_function5(self):
        input = """
        Var: printT;
        Function: printStrLn
        Body:
        EndBody.
        Function: main
        Body:
        EndBody.
                   """
        expect = str(Redeclared(Function(),"printStrLn"))
        self.assertTrue(TestChecker.test(input,expect,430))

    def test_type_cannot_be_inferred1(self):
        input = """
        Var: x;
        Function: main
        Body:
            Var: y;
            x = y;
        EndBody.
                   """
        expect = str(TypeCannotBeInferred(Assign(Id("x"),Id("y"))))
        self.assertTrue(TestChecker.test(input,expect,431))

    def test_type_cannot_be_inferred2(self):
        input = """
        Function: foo
        Parameter: x
        Body:
            Return 1;
        EndBody.
        Function: main
        Body:
            Var: y, a, x;
            y = a + foo(x);
        EndBody.
                   """
        expect = str(TypeCannotBeInferred(Assign(Id("y"),BinaryOp("+",Id("a"),CallExpr(Id("foo"),[Id("x")])))))
        self.assertTrue(TestChecker.test(input,expect,432))

    def test_type_cannot_be_inferred3(self):
        input = """
        Function: main
        Parameter: x[5], y
        Body:
            Var: a[5], z;
            x[5] = {1.,2.,3.,4.,5.};
            a = x;
            z = y;
        EndBody.
                   """
        expect = str(TypeMismatchInStatement(Assign(ArrayCell(Id("x"),[IntLiteral(5)]),ArrayLiteral([FloatLiteral(1.0),FloatLiteral(2.0),FloatLiteral(3.0),FloatLiteral(4.0),FloatLiteral(5.0)]))))
        self.assertTrue(TestChecker.test(input,expect,433))

    def test_type_cannot_be_inferred4(self):
        input = """
        Var: arr[5][2];
        Function: main
        Parameter: x[5][2], c
        Body:
            Var: str = "canBe";
            c = str;
            x = arr;
        EndBody.
                   """
        expect = str(TypeCannotBeInferred(Assign(Id("x"),Id("arr"))))
        self.assertTrue(TestChecker.test(input,expect,434))

    def test_type_cannot_be_inferred5(self):
        input = """
        Var: abc;
        Var: y;
        Function: main
        Parameter: x[5][4], y
        Body:
            Var: z, t=2;
            abc = "someThing";
            x[1][1] = 10;
            x[2][2] = x[1][1];
            y = x[t][t];
            Return 0;
        EndBody.
        Function: foo
        Body:
            Var: x, z;
            x = abc;
            y = z;
        EndBody.
                   """
        expect = str(TypeCannotBeInferred(Assign(Id("y"),Id("z"))))
        self.assertTrue(TestChecker.test(input,expect,435))

    def test_type_cannot_be_inferred6(self):
        input = """
        Function: main
        Parameter: a, b, c
        Body:
            Var: x[5][10], y[2][4];
            y[1][2] = 2.5;
            y[1][1] = c;
            x[3][9] = a;
            Return 0;
        EndBody.
                   """
        expect = str(TypeCannotBeInferred(Assign(ArrayCell(Id("x"),[IntLiteral(3),IntLiteral(9)]),Id("a"))))
        self.assertTrue(TestChecker.test(input,expect,436))

    def test_type_cannot_be_inferred7(self):
        input = """
        Function: main
        Body:
            Var: x;
            foo(True, x, False);
            Return 0;
        EndBody.
        Function: foo
        Parameter: p1, p2, p3
        Body:
            Return;
        EndBody.
                   """
        expect = str(TypeCannotBeInferred(CallStmt(Id("foo"),[BooleanLiteral(True),Id("x"),BooleanLiteral(False)])))
        self.assertTrue(TestChecker.test(input,expect,437))

    def test_type_cannot_be_inferred8(self):
        input = """
        Function: main
        Parameter: y
        Body:
            Var: x;
            main(x);
            Return;
        EndBody.
                   """
        expect = str(TypeCannotBeInferred(CallStmt(Id("main"),[Id("x")])))
        self.assertTrue(TestChecker.test(input,expect,438))

    def test_type_cannot_be_inferred9(self):
        input = """
        Function: main
        Parameter: x1[5]
        Body:
            Var: x2[2] = {1,2};
            foo(x1, x2, 1);
            Return;
        EndBody.
        Function: foo
        Parameter: p1[5], p2[2], p3
        Body:
            Return;
        EndBody.
                   """
        expect = str(TypeCannotBeInferred(CallStmt(Id("foo"),[Id("x1"),Id("x2"),IntLiteral(1)])))
        self.assertTrue(TestChecker.test(input,expect,439))

    def test_type_cannot_be_inferred10(self):
        input = """
        Function: main
        Parameter: arg1, arg2
        Body:
            Var: x, y = 2;
            x = main(y, True);
            Return x;
        EndBody.
                   """
        expect = str(TypeCannotBeInferred(Assign(Id("x"),CallExpr(Id("main"),[Id("y"),BooleanLiteral(True)]))))
        self.assertTrue(TestChecker.test(input,expect,440))

    def test_type_cannot_be_inferred11(self):
        input = """
        Function: main
        Parameter: arg1[3], arg2[20], arg3
        Body:
            Var: x[3] = {1,2,3};
            arg1[1] = 2;
            arg2[3] = 10;
            x = main(x, arg2, arg1[1] == arg2[3]);
            foo(arg3);
            Return x;
        EndBody.
        Function: foo
        Parameter: arg
        Body:
            Var: x[3], y[20], z;
            z = 2 + x[1] + main(x, y, arg)[2];
            foo2()[1] = 2;
            Return;
        EndBody.
        Function: foo2
        Body:
            Return {1,2};
        EndBody.
                   """
        expect = str(TypeCannotBeInferred(Assign(ArrayCell(CallExpr(Id("foo2"),[]),[IntLiteral(1)]),IntLiteral(2))))
        self.assertTrue(TestChecker.test(input,expect,441))

    def test_type_cannot_be_inferred12(self):
        input = """
        Function: main
        Body:
            Var: x;
            If True Then
                Var: x, y;
            EndIf.
            Return;
        EndBody.
                   """
        expect = str(TypeCannotBeInferred(If([(BooleanLiteral(True),[VarDecl(Id("x"),[],None),VarDecl(Id("y"),[],None)],[])],([],[]))))
        self.assertTrue(TestChecker.test(input,expect,442))

    def test_type_cannot_be_inferred13(self):
        input = """
        Function: main
        Body:
            Var: x;
            If True Then
                Var: x = 3;
            ElseIf False Then
                Var: y, z = 3;
            EndIf.
            Return;
        EndBody.
                   """
        expect = str(TypeCannotBeInferred(If([(BooleanLiteral(True),[VarDecl(Id("x"),[],IntLiteral(3))],[]),(BooleanLiteral(False),[VarDecl(Id("y"),[],None),VarDecl(Id("z"),[],IntLiteral(3))],[])],([],[]))))
        self.assertTrue(TestChecker.test(input,expect,443))

    def test_type_cannot_be_inferred14(self):
        input = """
        Function: main
        Body:
            Var: x;
            If True Then
                Var: s;
                print(s);
            Else 
                Var: x;
            EndIf.
            Return;
        EndBody.
                   """
        expect = str(TypeCannotBeInferred(If([(BooleanLiteral(True),[VarDecl(Id("s"),[],None)],[CallStmt(Id("print"),[Id("s")])])],([VarDecl(Id("x"),[],None)],[]))))
        self.assertTrue(TestChecker.test(input,expect,444))

    def test_type_cannot_be_inferred15(self):
        input = """
        Function: main
        Parameter: arg
        Body:
            Var: i;
            For (i = 0, i < 10, 2) Do
                Var: y;
                main(i);
            EndFor.
            Return;
        EndBody.
                   """
        expect = str(TypeCannotBeInferred(For(Id("i"),IntLiteral(0),BinaryOp("<",Id("i"),IntLiteral(10)),IntLiteral(2),([VarDecl(Id("y"),[],None)],[CallStmt(Id("main"),[Id("i")])]))))
        self.assertTrue(TestChecker.test(input,expect,445))

    def test_type_cannot_be_inferred16(self):
        input = """
        Function: main
        Parameter: arg
        Body:
            While True Do
                Var: x;
                printStrLn(x);
                While True Do
                    Var: x;
                EndWhile.
            EndWhile.
            Return;
        EndBody.
                   """
        expect = str(TypeCannotBeInferred(While(BooleanLiteral(True),([VarDecl(Id("x"),[],None)],[]))))
        self.assertTrue(TestChecker.test(input,expect,446))

    def test_type_cannot_be_inferred17(self):
        input = """
        Function: main
        Parameter: arg
        Body:
            Var: x;
            Do
                Var: str;
            While x   
            EndDo.
            Return;
        EndBody.
                   """
        expect = str(TypeCannotBeInferred(Dowhile(([VarDecl(Id("str"),[],None)],[]),Id("x"))))
        self.assertTrue(TestChecker.test(input,expect,447))

    def test_type_cannot_be_inferred18(self):
        input = """
        Function: main
        Body:
            Var: x;
            Return x;
        EndBody.
                   """
        expect = str(TypeCannotBeInferred(Return(Id("x"))))
        self.assertTrue(TestChecker.test(input,expect,448))

    def test_type_cannot_be_inferred19(self):
        input = """
        Function: main
        Body:
            Return main();
        EndBody.
                   """
        expect = str(TypeCannotBeInferred(Return(CallExpr(Id("main"),[]))))
        self.assertTrue(TestChecker.test(input,expect,449))

    def test_type_cannot_be_inferred30(self):
        input = """
        Function: main
        Body:
            Var: x[5];
            If True Then
                While True Do
                    Return x;
                EndWhile.
            EndIf.
        EndBody.
                   """
        expect = str(TypeCannotBeInferred(Return(Id("x"))))
        self.assertTrue(TestChecker.test(input,expect,450))

    def test_type_cannot_be_inferred20(self):
        input = """
        Var: x;
        Function: main
        Parameter: x, y
        Body:
            Return main(1, main(x, True));
        EndBody.
        Function: foo
        Body:
            Return main(1,2);
        EndBody.
                   """
        expect = str(TypeMismatchInExpression(CallExpr(Id("main"),[IntLiteral(1),IntLiteral(2)])))
        self.assertTrue(TestChecker.test(input,expect,451))

    def test_type_missmatch_in_stm1(self):
        input = """
        Function: main
        Body:
            Var: x;
            x = (2 == 0);
            If x Then
            ElseIf !x Then
            ElseIf 2 Then
            EndIf.
        EndBody.
                   """
        expect = str(TypeMismatchInStatement(If([(Id("x"),[],[]),(UnaryOp("!",Id("x")),[],[]),(IntLiteral(2),[],[])],([],[]))))
        self.assertTrue(TestChecker.test(input,expect,452))

    def test_type_missmatch_in_stm2(self):
        input = """
        Var: a = 10;
        Function: main
        Body:
            Var: x;
            If x Then
                While x Do
                    If 5 - a Then
                    EndIf.
                EndWhile.
            EndIf.
        EndBody.
                   """
        expect = str(TypeMismatchInStatement(If([(BinaryOp("-",IntLiteral(5),Id("a")),[],[])],([],[]))))
        self.assertTrue(TestChecker.test(input,expect,453))

    def test_type_missmatch_in_stm3(self):
        input = """
        Var: a[2];
        Function: main
        Body:
            Var: x;
            If a[1] Then
                While a[0] Do
                    If !x Then
                        If main() Then
                            If a Then
                            EndIf.
                        EndIf.
                    EndIf.
                EndWhile.
            EndIf.
        EndBody.
                   """
        expect = str(TypeMismatchInStatement(If([(Id("a"),[],[])],([],[]))))
        self.assertTrue(TestChecker.test(input,expect,454))

    def test_type_missmatch_in_stm4(self):
        input = """
        Function: main
        Body:
            Var: i;
            For (i = True, i < 10, 2) Do
            EndFor.
        EndBody.
                   """
        expect = str(TypeMismatchInStatement(For(Id("i"),BooleanLiteral(True),BinaryOp("<",Id("i"),IntLiteral(10)),IntLiteral(2),([],[]))))
        self.assertTrue(TestChecker.test(input,expect,455))

    def test_type_missmatch_in_stm30(self):
        input = """
        Function: main
        Body:
            Var: i = 10., k, j;
            For (k = j, j < 10, int_of_float(i)) Do
                For (i = 1, i <. 9., 2) Do
                EndFor.
            EndFor.
        EndBody.
                   """
        expect =  str(TypeMismatchInStatement(For(Id("i"),IntLiteral(1),BinaryOp("<.",Id("i"),FloatLiteral(9.0)),IntLiteral(2),([],[]))))
        self.assertTrue(TestChecker.test(input,expect,456))

    def test_type_missmatch_in_stm5(self):
        input = """
        Function: foo
        Body:
            Return 1.0;
        EndBody.
        Function: main
        Body:
            Var: flag;
            Do
                While !flag Do
                    While foo() Do
                    EndWhile.
                EndWhile.
            While flag EndDo.
        EndBody.
                   """
        expect =  str(TypeMismatchInStatement(While(CallExpr(Id("foo"),[]),([],[]))))
        self.assertTrue(TestChecker.test(input,expect,457))

    def test_type_missmatch_in_stm6(self):
        input = """
        Function: foo
        Body:
            Return;
        EndBody.
        Function: main
        Body:
            Var: x;
            x = foo();
            Return 0;
        EndBody.
                   """
        expect =  str(TypeMismatchInStatement(Assign(Id("x"),CallExpr(Id("foo"),[]))))
        self.assertTrue(TestChecker.test(input,expect,458))

    def test_type_missmatch_in_stm31(self):
        input = """
        Function: main
        Body:
            Var: x;
            foo(1,2);
            x = foo(5,99);
            Return 0;
        EndBody.
        Function: foo
        Parameter: x1, x2
        Body:
            Return;
        EndBody.
                   """
        expect = str(TypeMismatchInStatement(Assign(Id("x"),CallExpr(Id("foo"),[IntLiteral(5),IntLiteral(99)]))))
        self.assertTrue(TestChecker.test(input,expect,459))

    def test_type_missmatch_in_stm7(self):
        input = """
        Var: abc[10][10];
        Function: main
        Body:
            Var: x[3][10];
            abc[foo(5)][x[1][2]] = 9;
            x[1][1] = abc[2][2];
            x = abc;
            Return 0;
        EndBody.
        Function: foo
        Parameter: x
        Body:
            Return 1;
        EndBody.
                   """
        expect = str(TypeMismatchInStatement(Assign(Id("x"),Id("abc"))))
        self.assertTrue(TestChecker.test(input,expect,460))

    def test_type_missmatch_in_stm8(self):
        input = """
        Var: arr1[10][10];
        Var: arr2[2][2];
        Function: main
        Body:
            Var: x[3][1], y[3][1];
            x = {{2.},{1.},{0.5}};
            x = y;
            arr2 = {{1,2},{3,4}};
            arr1[2][4] = arr2[1][1]; 
            arr1 = {{1,2},{3,4}};
            Return 0;
        EndBody.
        Function: foo
        Parameter: x
        Body:
            Return 1;
        EndBody.
                   """
        expect = str(TypeMismatchInStatement(Assign(Id("arr1"),ArrayLiteral([ArrayLiteral([IntLiteral(1),IntLiteral(2)]),ArrayLiteral([IntLiteral(3),IntLiteral(4)])]))))
        self.assertTrue(TestChecker.test(input,expect,461))

    def test_type_missmatch_in_stm9(self):
        input = """
        Function: foo
        Body:
            Var: x[5][5][10];
            x[1][2][4] = "BK";
            Return x;
        EndBody.
        Function: main
        Body:
            Var: x, y, z[5][5][10], t[5][5][10];
            x = foo()[1][2][4];
            y = int_of_string(x);
            z = foo();
            t[int_of_string(x)][y][y + int_of_string(x)] = 2;
            t = foo();
            Return 0;
        EndBody.
                   """
        expect = str(TypeMismatchInStatement(Assign(Id("t"),CallExpr(Id("foo"),[]))))
        self.assertTrue(TestChecker.test(input,expect,462))

    def test_type_missmatch_in_stm10(self):
        input = """
        Function: main
        Body:
            Var: x;
            x = foo() + x;
            foo();
            Return 0;
        EndBody.
        Function: foo
        Body:
            print("hi");
        EndBody.
                   """
        expect = str(TypeMismatchInStatement(CallStmt(Id("foo"),[])))
        self.assertTrue(TestChecker.test(input,expect,463))

    def test_type_missmatch_in_stm11(self):
        input = """
        Function: main
        Body:
            Var: x, y;
            x = 2. \. foo(1., 2.);
            y = foo(x, x, x) +. 2.;
            Return 0;
        EndBody.
        Function: foo
        Parameter: x, y
        Body:
            Return float_to_int(1);
        EndBody.
                   """
        expect = str(TypeMismatchInExpression(CallExpr(Id("foo"),[Id("x"),Id("x"),Id("x")])))
        self.assertTrue(TestChecker.test(input,expect,464))

    def test_type_missmatch_in_stm12(self):
        input = """
        Function: main
        Parameter: x1[5], x2
        Body:
            Var: x, y;
            x =  x + main({1.,2.,3.,4.,5.} , 2) + x2;
            x2 = 1;
            x1[1] = 1;
            Return 0;
        EndBody.
                   """
        expect = str(TypeMismatchInStatement(Assign(ArrayCell(Id("x1"),[IntLiteral(1)]),IntLiteral(1))))
        self.assertTrue(TestChecker.test(input,expect,465))

    def test_type_missmatch_in_stm13(self):
        input = """
        Function: main
        Body:
            foo();
            Return 0;
        EndBody.
        Function: foo
        Body:
            Return True && False;
        EndBody.
                   """
        expect = str(TypeMismatchInStatement(Return(BinaryOp("&&",BooleanLiteral(True),BooleanLiteral(False)))))
        self.assertTrue(TestChecker.test(input,expect,466))

    def test_type_missmatch_in_stm13(self):
        input = """
        Var: abc[5];
        Var: boo[2] = {True, False};
        Function: main
        Body:
            Var: x[5] = {1,2,3,4,5};
            While (boo[1]) Do
                Return x;
            EndWhile.
            If (boo[0]) Then
                Return abc;
            EndIf.
            Return 0;
        EndBody.
                   """
        expect = str(TypeMismatchInStatement(Return(IntLiteral(0))))
        self.assertTrue(TestChecker.test(input,expect,467))

    def test_type_missmatch_in_exp1(self):
        input = """
        Function: main
        Body:
            Var: x[100][200][300];
            x[100][1][3] = 2 * x[foo(1)][2][3];
            x[foo(x[100][1][2])][2][foo(x[22][33][44])] = 2;
            x[12] = 1;
        EndBody.
        Function: foo
        Parameter: x
        Body:
            
        EndBody.
                   """
        expect = str(TypeMismatchInExpression(ArrayCell(Id("x"),[IntLiteral(12)])))
        self.assertTrue(TestChecker.test(input,expect,468))

    def test_type_missmatch_in_exp2(self):
        input = """
        Var: x[10][20];
        Function: main
        Body:
            Var: x;
            If True Then
                x[2][3] = True;
            EndIf.
            Return 0;
        EndBody.
                   """
        expect = str(TypeMismatchInExpression(ArrayCell(Id("x"),[IntLiteral(2),IntLiteral(3)])))
        self.assertTrue(TestChecker.test(input,expect,469))

    def test_type_missmatch_in_exp3(self):
        input = """
        Function: main
        Body:
            Var: x[3][4][5];
            While True Do
                Var: x[3][4];
                x[1][3] = True;
            EndWhile.
            x[x[2][3]][3][4] = 2;
            Return 0;
        EndBody.
                   """
        expect = str(TypeMismatchInExpression(ArrayCell(Id("x"),[IntLiteral(2),IntLiteral(3)])))
        self.assertTrue(TestChecker.test(input,expect,470))

    def test_type_missmatch_in_exp4(self):
        input = """
        Function: main
        Body:
            Var: x[3], y, z, t;
            x[2] = 2. +. y +. z;
            x[1] = 1. +. y \. 3.;
            t = x[1] \ 2;
            Return 0;
        EndBody.
                   """
        expect = str(TypeMismatchInExpression(BinaryOp("\\",ArrayCell(Id("x"),[IntLiteral(1)]),IntLiteral(2))))
        self.assertTrue(TestChecker.test(input,expect,471))

    def test_type_missmatch_in_exp5(self):
        input = """
        Function: main
        Parameter: x, y
        Body:
            Var: a, b, c, d, e;
            main(a =/= b, int_of_float(a) + int_of_float(b));
            c = bool_of_string("true");
            e = !c && c || d && !x || (y >. 12e5);
            
            Return 0;
        EndBody.
                   """
        expect = str(TypeMismatchInExpression(BinaryOp(">.",Id("y"),FloatLiteral(1200000.0))))
        self.assertTrue(TestChecker.test(input,expect,472))

    def test_type_missmatch_in_exp6(self):
        input = """
        Function: main
        Parameter: x
        Body:
            Var: a, b, c;
            main(a +. 3. -. 2. *. 2.);
            b = x;
            c = (a \. 3.51242) * (b + 2); 
            Return 0;
        EndBody.
                   """
        expect = str(TypeMismatchInExpression(BinaryOp("+",Id("b"),IntLiteral(2))))
        self.assertTrue(TestChecker.test(input,expect,473))

    def test_type_missmatch_in_exp7(self):
        input = """
        Function: main
        Parameter: x
        Body:
            Var: z, y;
            z = 1 + main(-(2 + main(2)));
            z = y + x;
            y = -(y\z) + -x + float_to_int(main(1));
            Return 0;
        EndBody.
                   """
        expect = str(TypeMismatchInExpression(BinaryOp("+",BinaryOp("+",UnaryOp("-",BinaryOp("\\",Id("y"),Id("z"))),UnaryOp("-",Id("x"))),CallExpr(Id("float_to_int"),[CallExpr(Id("main"),[IntLiteral(1)])]))))
        self.assertTrue(TestChecker.test(input,expect,474))

    def test_type_missmatch_in_exp8(self):
        input = """
        Function: main
        Parameter: x
        Body:
            Var: t, x1;
            t = 1 + foo(main(x +. 2.5) \. 68.21, 2, 3, 4, 5);
            x1 = foo(x,91,36,42,59);
            x1 = foo(x1, 5, 10, 15, 20);
            Return 0;
        EndBody.
        Function: foo
        Parameter: f1, f2, f3, f4, f5
        Body:
        EndBody.
                   """
        expect = str(TypeMismatchInExpression(CallExpr(Id("foo"),[Id("x1"),IntLiteral(5),IntLiteral(10),IntLiteral(15),IntLiteral(20)])))
        self.assertTrue(TestChecker.test(input,expect,475))

    def test_type_missmatch_in_exp9(self):
        input = """
        Function: foo
        Parameter: e[1], f
        Body:
            e[0] = True;
        EndBody.
        Function: main
        Parameter: x
        Body:
            x = foo({3}, True);
            Return 0;
        EndBody.
                   """
        expect = str(TypeMismatchInExpression(CallExpr(Id("foo"),[ArrayLiteral([IntLiteral(3)]),BooleanLiteral(True)])))
        self.assertTrue(TestChecker.test(input,expect,476))

    def test_no_entry_point1(self):
        input = """
        Var: main;
        Function: foo
        Parameter: main
        Body:
            Return 0;
        EndBody.
                   """
        expect = str(NoEntryPoint())
        self.assertTrue(TestChecker.test(input,expect,477))

    def test_no_entry_point2(self):
        input = """
        Function: main1
        Parameter: main
        Body:
            main = "main";
            Return main;
        EndBody.
        Function: main2
        Parameter: main
        Body:
            Return 0;
        EndBody.
                   """
        expect = str(NoEntryPoint())
        self.assertTrue(TestChecker.test(input,expect,478))
    
    def test_full_program1(self):
        input = """
        Function: foo
        Parameter: f
        Body:
            Return 0;
        EndBody.
        Function: main
        Body:
            Var: i, j, k, l, n;
            Do 
                i = i + 1;
                While (j < 100) Do
                    Do
                        k = k + 1;
                        While (l < 100) Do
                            l = l + 2;
                            n = l \ 2;
                        EndWhile.
                    While (k < 100) EndDo.
                    j = j + 3;
                EndWhile.
            While (i + j + k + l < foo(2)) EndDo.
            print(n);
        EndBody.
                   """
        expect = str(TypeMismatchInStatement(CallStmt(Id("print"),[Id("n")])))
        self.assertTrue(TestChecker.test(input,expect,479))

    def test_full_program2(self):
        input = """
        Var: s = 0, arr[2] = {1,2};
        Function: combat
        Parameter: hp1, hp2, d
        **// TODO: You have to complete this function followed by requirements**
        Body:
            Var: p1, p2;
            Var: h1, h2;
            Var: none = False;
            Var: pR;
            p1 = float_to_int(hp1 * (1000 - d) \ int_of_float(1000.));
            p2 = float_to_int((hp2 * d) \ int_of_float(1000.));
            h1 = (hp1 + hp2) % 100;
            h2 = (h1*hp2) % 100;
             
            If (hp2 == 888) Then none = True;
            EndIf.
            If (hp1 == 777) && ((p1 <. p2) || (h1 < h2)) && (none) Then
                Var: e = 1;
                d = e;
                p1 = float_to_int(hp1) *. float_to_int(1000 - d) \. float_to_int(1000);
                p2 = float_to_int((hp2 * 1) \ 1000);
            EndIf.
            pR = p1 *. p2;
            print(pR);
        EndBody.
        Function: main
        Body:
            combat(544,290,600);
        EndBody. """
        expect = str(TypeMismatchInStatement(CallStmt(Id("print"),[Id("pR")])))
        self.assertTrue(TestChecker.test(input,expect,480))

    def test_full_program3(self):
        input = """
        Var: s, arr[2];
        Function: combat
        Parameter: s1, s2
        Body:
            Var: x, y, z;
            If z Then
                Var: y;
                x = 1;
                y = 2;
            Else
                x = y;
                s = z;
                arr[1] = z;
            EndIf.
            Return;
        EndBody.
        Function: main
        Body:
            Var: m1, m2;
            m1 = s;
            m2 = arr;
            Return 0;
        EndBody. """
        expect = str(TypeMismatchInStatement(Assign(Id("m2"),Id("arr"))))
        self.assertTrue(TestChecker.test(input,expect,481))

    def test_full_program4(self):
        input = """
        Var: x[2][3][4], y[22];
        Function: foo
        Parameter: s1, s2
        Body:
            Var: x;
            x = s1 + s2 + foo(s1, s2);
            Return x;
        EndBody.
        Function: main
        Body:
            main();
            foo()[10] = 2;
            Return;
        EndBody. """
        expect = str(TypeMismatchInExpression(CallExpr(Id("foo"),[])))
        self.assertTrue(TestChecker.test(input,expect,482))

    def test_full_program5(self):
        input = """
        Var: x[2][3];
        Function: foo
        Parameter: s1, s2
        Body:
            x[1][1] = True;
            Return x;
        EndBody.
        Function: main
        Parameter: x1, x2
        Body:
            While foo(1,2)[1][2] Do
                Var: x;
                main(1, foo(4,5)[1][1]);
                For (x = x1, x2, 2) Do
                    Var: x;
                    x = 1.2453;
                    If foo(4,5)[1][1] && foo(1,2)[1][2] Then
                        print(string_of_float(x));
                    EndIf.
                EndFor.
            EndWhile.
            Return foo(4,5);
        EndBody. """
        expect = str(TypeMismatchInStatement(Return(CallExpr(Id("foo"),[IntLiteral(4),IntLiteral(5)]))))
        self.assertTrue(TestChecker.test(input,expect,483))

    def test_full_program6(self):
        input = """
        Var: x[2][3] = {{3.,4.,2.51},{12e2,12e1,6e5}};
        Function: main
        Parameter: s1, s2
        Body:
            main(1., True);
            x = foo(s1, s2);
            Return;
        EndBody.
        Function: foo
        Parameter: s1, s2
        Body:
            Var: y[2][3];
            If True Then
                Return y;
            ElseIf False Then
                Return x;
            Else
                Return foo(x,2);
            EndIf.
        EndBody.
        """
        expect = str(TypeMismatchInExpression(CallExpr(Id("foo"),[Id("x"),IntLiteral(2)])))
        self.assertTrue(TestChecker.test(input,expect,484))

    def test_full_program7(self):
        input = """
        Var: x;
        Function: fact
        Parameter: n
        Body:
            If n == 0 Then
                Return 1;
            Else
                Return n * fact (n - 1);
            EndIf.
        EndBody.
        Function: main
        Body:
            x = 10;
            fact(x);
        EndBody.
        """
        expect = str(TypeMismatchInStatement(CallStmt(Id("fact"),[Id("x")])))
        self.assertTrue(TestChecker.test(input,expect,485))

    def test_full_program8(self):
        input = """
        Function: main
        Parameter: x
        Body:
            Var: arr[10][10];
            Var: i, j;
            For (i = 0, i < 10, 1) Do  
                For (j = 0, j < 10, 1) Do
                    arr[i][j] = 0;
                EndFor.
            EndFor.
            x = -.arr[2][2];
            Return 0;
        EndBody.
        """
        expect = str(TypeMismatchInExpression(UnaryOp("-.",ArrayCell(Id("arr"),[IntLiteral(2),IntLiteral(2)]))))
        self.assertTrue(TestChecker.test(input,expect,486))

    def test_full_program9(self):
        input = """
        Function: main
        Body:
            Var: a = 3, b = 4, c = 5;
            If (a < b + c) && ( b < a + c) && ( c < a + b) Then
                If (a*a==b*b+c*c) || (b*b==a*a+c*c) || (c*c== a*a+b*b) Then
                    print("Day la tam giac vuong");
                EndIf.
            ElseIf (a==b) && (b==c) Then print("Day la tam giac deu");
            ElseIf (a==b) || (a==c) || (b==c) Then print("Day la tam giac can");
            ElseIf (a*a > b*b+c*c) || (b*b > a*a+c*c) || (c*c > a*a+b*b) Then print("Day la tam giac tu");
            Else print("Day la tam giac nhon");
            EndIf.
            Return main();
        EndBody.
        """
        expect = str(TypeCannotBeInferred(Return(CallExpr(Id("main"),[]))))
        self.assertTrue(TestChecker.test(input,expect,487))

    def test_full_program10(self):
        input = """
        Function: main **1 + 2 + ... n < max**
        Parameter: max
        Body:
            Var: n = 0, s = 0;
            Do 
                n = n + 1;
                s = s + n;
            While s + n + 1 < max EndDo.
            writeln(n);
        EndBody.
        """
        expect = str(Undeclared(Function(),"writeln"))
        self.assertTrue(TestChecker.test(input,expect,488))

    def test_full_program11(self):
        input = """
        Var: s = "ppL2020";
        Function: fibonacci
        Parameter: n
        Body:
            If (n == 1) || (n == 2) Then
                Return 1;
            EndIf.
            Return fibonacci(n - 1) + fibonacci(n - 2);
        EndBody.
        Function: adventure
        Parameter: nEvents
        Body:
            Var: i;
            For (i = 0, i < nEvents, 1) Do
                If i == nEvents \ 5 Then 
                    Return fibonacci(int_of_float(2222.1));
                EndIf.
            EndFor.
        EndBody.
        Function: main
        Body:
            adventure(1023);
        EndBody.
        """
        expect = str(TypeMismatchInStatement(CallStmt(Id("adventure"),[IntLiteral(1023)])))
        self.assertTrue(TestChecker.test(input,expect,489))

    def test_full_program12(self):
        input = """
        Var: abc[2][2][3];
        Function: main
        Body:
            Var: athos = 500, pothos = 900, jerry, tom = 200;
            If (pothos - athos) < 400 Then jerry = pothos - tom;
            Else jerry = athos - tom;
            EndIf.
            Return abc;
        EndBody.
        """
        expect = str(TypeCannotBeInferred(Return(Id("abc"))))
        self.assertTrue(TestChecker.test(input,expect,490))

    def test_full_program13(self):
        input = """
        Var: main;
        Function: foo
        Body:
            Var: num = 10;
            If num > 0 Then print("Positive number");
            Else 
                If num == 0 Then print("Zero");
                Else print("Negative number");
                EndIf.
            EndIf.
        EndBody.
        """
        expect = str(NoEntryPoint())
        self.assertTrue(TestChecker.test(input,expect,491))

    def test_full_program14(self):
        input = """
        Var: x, y;
        Function: main
        Body:
            Var: i = 20, a, b, c;
            If i == 10 Then 
                a = 1;
                b = 2;
                c = a + b;
                x = c;
            ElseIf i == 15 Then
                a = 3;
                b = 4;
                c = b - a;
            ElseIf i == 20 Then
                a = 2;
                b = 2;
                c = a*2 + b*3;
            EndIf.
            y = (x+a)*(x+b)*(x+.2.);
            Return 0;
        EndBody.
        """
        expect = str(TypeMismatchInExpression(BinaryOp("+.",Id("x"),FloatLiteral(2.0))))
        self.assertTrue(TestChecker.test(input,expect,492))

    def test_full_program16(self):
        input = """
        Var: abc[12][22][33][44][55];
        Function: main
        Parameter: max
        Body:
            Var: x;
            max = 1;
            x = main(abc[main(23)][main(33)][main(44)][main(55)][main(x)]);
            x = 2.0;
            Return 0;
        EndBody.
        """
        expect = str(TypeMismatchInStatement(Assign(Id("x"),FloatLiteral(2.0))))
        self.assertTrue(TestChecker.test(input,expect,493))

    def test_full_program17(self):
        input = """
        Function: main 
        Parameter: s1, s2, s3
        Body: 
            Return 1 + main(s1 + 1, s2 \. 2.0, s3 + s1);
        EndBody.
        Function: foo
        Body: 
            main(2, 2.0, 3);
        EndBody.
        """
        expect = str(TypeMismatchInStatement(CallStmt(Id("main"),[IntLiteral(2),FloatLiteral(2.0),IntLiteral(3)])))
        self.assertTrue(TestChecker.test(input,expect,494))

    def test_full_program18(self):
        input = """
        Function: main 
        Parameter: s1, s2, s3
        Body: 
            print(string_of_int(main(1, 2, main(1, 2, 3))));
            printLn();
            Return read();
        EndBody.
        """
        expect = str(TypeMismatchInStatement(Return(CallExpr(Id("read"),[]))))
        self.assertTrue(TestChecker.test(input,expect,495))

    def test_full_program19(self):
        input = """
        Var: arr[2][3];
        Function: main
        Parameter: x
        Body:
            arr[1][2] = x + main(2.0);
        EndBody.
        """
        expect = str(TypeMismatchInExpression(CallExpr(Id("main"),[FloatLiteral(2.0)])))
        self.assertTrue(TestChecker.test(input,expect,496))

    def test_full_program20(self):
        input = """
        Function: main
        Body:
            printLn();
            print("Ass3");
            If True Then
                Var: print = 0;
            Else
                print("ass3");
            EndIf.
            While bool_of_string("ass3") Do
                Var: print;
                print("ass3");
            EndWhile.
            Return 0;
        EndBody.
        """
        expect = str(Undeclared(Function(),"print"))
        self.assertTrue(TestChecker.test(input,expect,497))

    def test_full_program21(self):
        input = """
        Var: a[2][2] = {{3,4},{1,2}};
        Function: main
        Body:
            a = foo();
            Return int_of_float(float_to_int(foo()[1][1]));
        EndBody.
        Function: foo
        Body:
            Return;
        EndBody.
        """
        expect = str(TypeMismatchInStatement(Return(None)))
        self.assertTrue(TestChecker.test(input,expect,498))

    def test_full_program22(self):
        input = """
        Var: arr[3][5];
        Function: main
        Parameter: x, y, z
        Body:
            arr[2][1] = "2.41";
            arr[1*y][2*z] = x +. main(float_of_string(arr[2][1]), 3, 2);
        EndBody.
        """
        expect = str(TypeMismatchInStatement(Assign(ArrayCell(Id("arr"),[BinaryOp("*",IntLiteral(1),Id("y")),BinaryOp("*",IntLiteral(2),Id("z"))]),BinaryOp("+.",Id("x"),CallExpr(Id("main"),[CallExpr(Id("float_of_string"),[ArrayCell(Id("arr"),[IntLiteral(2),IntLiteral(1)])]),IntLiteral(3),IntLiteral(2)])))))
        self.assertTrue(TestChecker.test(input,expect,499))

    def test_diff_numofparam_stmt(self):
        """Complex program"""
        input = """Function: main  
                   Body:
                        printStrLn();
                    EndBody."""
        expect = str(TypeMismatchInStatement(CallStmt(Id("printStrLn"),[])))
        self.assertTrue(TestChecker.test(input,expect,500))
    
    def test_diff_numofparam_expr(self):
        """More complex program"""
        input = """Function: main 
                    Body:
                        printStrLn(read(4));
                    EndBody."""
        expect = str(TypeMismatchInExpression(CallExpr(Id("read"),[IntLiteral(4)])))
        self.assertTrue(TestChecker.test(input,expect,400))

    def test_undeclared_function_use_ast(self):
        """Simple program: main """
        input = Program([FuncDecl(Id("main"),[],([],[
            CallExpr(Id("foo"),[])]))])
        expect = str(Undeclared(Function(),"foo"))
        self.assertTrue(TestChecker.test(input,expect,404))

    def test_diff_numofparam_expr_use_ast(self):
        """More complex program"""
        input = Program([
                FuncDecl(Id("main"),[],([],[
                    CallStmt(Id("printStrLn"),[
                        CallExpr(Id("read"),[IntLiteral(4)])
                        ])]))])
        expect = str(TypeMismatchInExpression(CallExpr(Id("read"),[IntLiteral(4)])))
        self.assertTrue(TestChecker.test(input,expect,402))

    def test_diff_numofparam_stmt_use_ast(self):
        """Complex program"""
        input = Program([
                FuncDecl(Id("main"),[],([],[
                    CallStmt(Id("printStrLn"),[])]))])
        expect = str(TypeMismatchInStatement(CallStmt(Id("printStrLn"),[])))
        self.assertTrue(TestChecker.test(input,expect,403))