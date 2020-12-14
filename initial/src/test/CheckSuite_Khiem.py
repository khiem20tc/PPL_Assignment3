import unittest
from TestUtils import TestChecker
from StaticError import *
from AST import *

class CheckSuite(unittest.TestCase):

    def test_undeclared_function(self):
        """Simple program: main"""
        input = """Function: main
                   Body:
                        foo();
                   EndBody."""
        expect = str(Undeclared(Function(),"foo"))
        self.assertTrue(TestChecker.test(input,expect,400))

    def test_diff_numofparam_stmt(self):
        """Complex program"""
        input = """Function: main
                   Body:
                        printStrLn();
                    EndBody."""
        expect = str(TypeMismatchInStatement(CallStmt(Id("printStrLn"),[])))
        self.assertTrue(TestChecker.test(input,expect,401))

    def test_diff_numofparam_expr(self):
        """More complex program"""
        input = """Function: main
                    Body:
                        printStrLn(read(4));
                    EndBody."""
        expect = str(TypeMismatchInExpression(CallExpr(Id("read"),[IntLiteral(4)])))
        self.assertTrue(TestChecker.test(input,expect,402))

    def test_undeclared_function_use_ast(self):
        """Simple program: main """
        input = Program([FuncDecl(Id("main"),[],([],[
            CallExpr(Id("foo"),[])]))])
        expect = str(Undeclared(Function(),"foo"))
        self.assertTrue(TestChecker.test(input,expect,403))

    def test_diff_numofparam_expr_use_ast(self):
        """More complex program"""
        input = Program([
                FuncDecl(Id("main"),[],([],[
                    CallStmt(Id("printStrLn"),[
                        CallExpr(Id("read"),[IntLiteral(4)])
                        ])]))])
        expect = str(TypeMismatchInExpression(CallExpr(Id("read"),[IntLiteral(4)])))
        self.assertTrue(TestChecker.test(input,expect,404))

    def test_diff_numofparam_stmt_use_ast(self):
        """Complex program"""
        input = Program([
                FuncDecl(Id("main"),[],([],[
                    CallStmt(Id("printStrLn"),[])]))])
        expect = str(TypeMismatchInStatement(CallStmt(Id("printStrLn"),[])))
        self.assertTrue(TestChecker.test(input,expect,405))




    def test_undeclared_function6(self):
        """Simple program: main"""
        input = """Var: a,c;
        Function: main
        Parameter: a,x,y
        Body:
        m=1;
        EndBody.
        """
        expect = str(Undeclared(Identifier(),"m"))
        self.assertTrue(TestChecker.test(input,expect,406))

    def test_undeclared_function7(self):
        """Simple program: main"""
        input = """Var: a,c;
        Function: main
        Parameter: a,x,y
        Body:
        a=c;
        EndBody.
        """
        expect = str(str(TypeCannotBeInferred(Assign(Id("a"),Id("c")))))
        self.assertTrue(TestChecker.test(input,expect,407))

    def test_undeclared_function8(self):
        """Simple program: main"""
        input = """Var: a,c;
        Function: main
        Parameter: a,x,y
        Body:
        a=m;
        EndBody.
        """
        expect = str(Undeclared(Identifier(),"m"))
        self.assertTrue(TestChecker.test(input,expect,408))

    def test_undeclared_function9(self):
        """Simple program: main"""
        input = """Var: a=1,c;
        Function: main
        Parameter: a,x,y
        Body:
        c=a;
        EndBody.
        """
        expect = str(TypeCannotBeInferred(Assign(Id("c"),Id("a"))))
        self.assertTrue(TestChecker.test(input,expect,409))

    def test_undeclared_function10(self):
        """Simple program: main"""
        input = """Var: a=1,c="hello";
        Function: main
        Parameter: a,x,y
        Body:
        c=a;
        EndBody.
        """
        expect = str()
        self.assertTrue(TestChecker.test(input,expect,410))

    def test_undeclared_function11(self):
        """Simple program: main"""
        input = """Var: a,b;
        Function: x
        Body:
        EndBody.
        """
        expect = str(NoEntryPoint())
        self.assertTrue(TestChecker.test(input,expect,411))

    def test_undeclared_function12(self):
        """Simple program: main"""
        input = """Var: a,b;
        Function: x
        Body:
        Var: m,n;
        EndBody.
        Function: main
        Body:
        Var: q,w;
        EndBody.
        """
        expect = str()
        self.assertTrue(TestChecker.test(input,expect,412))

    def test_undeclared_function13(self):
        """Simple program: main"""
        input = """Var: a,b;
        Function: x
        Parameter: h,k,l
        Body:
        Var: m,n;
        EndBody.
        Function: y
        Body:
        Var: q,w;
        EndBody.
        """
        expect = str(NoEntryPoint())
        self.assertTrue(TestChecker.test(input,expect,413))

    def test_undeclared_function14(self):
        """Simple program: main"""
        input = """Var: a,b;
        Function: hi
        Parameter: a,y
        Body:
        Var: x;
        EndBody.
        """
        expect = str(NoEntryPoint())
        self.assertTrue(TestChecker.test(input,expect,414))

    def test_undeclared_function15(self):
        """Simple program: main"""
        input = """Var: a,b;
        Function: hi
        Parameter: a,y
        Body:
        Var: x;
        EndBody.
        Function: hi
        Body:
        Var: k;
        EndBody.
        """
        expect = str(Redeclared(Function(),"hi"))
        self.assertTrue(TestChecker.test(input,expect,415))

    def test_undeclared_function16(self):
        """Simple program: main"""
        input = """
        Function: main
        Parameter: a,x,y
        Body:
        Var: k,l;
        k=2;
        l="string";
        k=l;
        EndBody.
        """
        expect = str(TypeMismatchInStatement(Assign(Id("k"),Id("l"))))
        self.assertTrue(TestChecker.test(input,expect,416))

    def test_undeclared_function17(self):
        """Simple program: main"""
        input = """
        Function: main
        Parameter: a,x,y
        Body:
        Var: k,l;
        k=0.1;
        l=k;
        EndBody.
        """
        expect = str()
        self.assertTrue(TestChecker.test(input,expect,417))

    def test_undeclared_function18(self):
        """Simple program: main"""
        input = """
        Var: l,k=0.1,m="string";
        Function: main
        Body:
        l=k;
        EndBody.
        """
        expect = str()
        self.assertTrue(TestChecker.test(input,expect,418))

    def test_undeclared_function19(self):
        """Simple program: main"""
        input = """
        Function: main
        Body:
        Var: a;
        a = -True;
        EndBody.
        """
        expect = str(TypeMismatchInExpression(UnaryOp("-",BooleanLiteral("true"))))
        self.assertTrue(TestChecker.test(input,expect,419))

    def test_undeclared_function20(self):
        """Simple program: main"""
        input = """
        Function: main
        Body:
        Var: a;
        a = 2+True;
        EndBody.
        """
        expect = str(TypeMismatchInExpression(BinaryOp("+",IntLiteral(2),BooleanLiteral("true"))))
        self.assertTrue(TestChecker.test(input,expect,420))

    def test_undeclared_function21(self):
        """Simple program: main"""
        input = """
        Function: main
        Body:
        Var: x=3;
        If x>1 Then x=x-1;
        EndIf.
        EndBody.
        """
        expect = str()
        self.assertTrue(TestChecker.test(input,expect,421))

    def test_undeclared_function22(self):
        """Simple program: main"""
        input = """
        Function: main
        Body:
        Var: x=3,a=1;
        If a+2 Then
        x=x+1;
        EndIf.
        EndBody.
        """
        expect = str(TypeMismatchInStatement(If([(BinaryOp("+",Id("a"),IntLiteral(2)),[],[Assign(Id("x"),BinaryOp("+",Id("x"),IntLiteral(1)))])],([],[]))))
        self.assertTrue(TestChecker.test(input,expect,422))

    def test_undeclared_function23(self):
        """Simple program: main"""
        input = """
        Function: main
        Body:
        Var: x=0, i=1;
        For (i=1, i<10, **test comment** 1) Do
            x=2+1;
        EndFor.
        EndBody.
        """
        expect = str()
        self.assertTrue(TestChecker.test(input,expect,423))

    def test_undeclared_function24(self):
        """Simple program: main"""
        input = """
        Function: main
        Body:
        Var: x=0, i;
        For (i=1, i+2, **test comment** 1) Do
            Break;
        EndFor.
        EndBody.
        """
        expect = str(TypeMismatchInStatement(For(Id("i"),IntLiteral(1),BinaryOp("+",Id("i"),IntLiteral(2)),IntLiteral(1),([],[Break()]))))
        self.assertTrue(TestChecker.test(input,expect,424))

    def test_undeclared_function25(self):
        """Simple program: main"""
        input = """
        Var: a,b,c;
        Function: main
        Body:
        Var: x,y;
        Return;
        EndBody.
        """
        expect = str()
        self.assertTrue(TestChecker.test(input,expect,425))

    def test_undeclared_function26(self):
        """Simple program: main"""
        input = """
        Var: a,b,c;
        Function: main
        Body:
        Var: x,y;
        Return 1;
        EndBody.
        """
        expect = str()
        self.assertTrue(TestChecker.test(input,expect,426))

    def test_undeclared_function27(self):
        """Simple program: main"""
        input = """
        Var: a,b=1;
        Function: main
        Body:
        a = a + b;
        EndBody.
        """
        expect = str()
        self.assertTrue(TestChecker.test(input,expect,427))

    def test_undeclared_function28(self):
        """Simple program: main"""
        input = """
        Var: a,b=1;
        Function: main
        Body:
        b = -a;
        EndBody.
        """
        expect = str()
        self.assertTrue(TestChecker.test(input,expect,428))

    def test_undeclared_function29(self):
        """Simple program: main"""
        input = """
        Var: a,b=1,c,d;
        Function: main
        Body:
        a = b+(c+d);
        EndBody.
        """
        expect = str()
        self.assertTrue(TestChecker.test(input,expect,429))

    def test_undeclared_function30(self):
        """Simple program: main"""
        input = """
        Var: a[1][1]={1,"str",3.2};
        Function: main
        Body:
        EndBody.
        """
        expect = str()
        self.assertTrue(TestChecker.test(input,expect,430))

    def test_undeclared_function31(self):
        """Simple program: main"""
        input = """
        Var: x,y;
        Function: main
        Parameter: a,b,c
        Body:
        EndBody.
        """
        expect = str()
        self.assertTrue(TestChecker.test(input,expect,431))

    def test_undeclared_function32(self):
        """Simple program: main"""
        input = """
        Function: foo
        Parameter: x,y
        Body:
        EndBody.
        Function: main
        Body:
        fo(1,2);
        EndBody.
        """
        expect = str(Undeclared(Function(),"fo"))
        self.assertTrue(TestChecker.test(input,expect,432))

    def test_undeclared_function33(self):
        """Simple program: main"""
        input = """
        Var: x,y;
        Function: foo
        Parameter: x,y
        Body:
        EndBody.
        Function: main
        Body:
        m(1,2);
        EndBody.
        """
        expect = str(Undeclared(Function(),"m"))
        self.assertTrue(TestChecker.test(input,expect,433))

    def test_undeclared_function34(self):
        """Simple program: main"""
        input = """
        Var: a;
        Function: foo
        Parameter: x,y,z
        Body:
        Var: b;
        EndBody.
        Function: main
        Body:
        Var: c;
        foo(1,2,3);
        EndBody.
        """
        expect = str()
        self.assertTrue(TestChecker.test(input,expect,434))

    def test_undeclared_function35(self):
        """Simple program: main"""
        input = """
        Var: a;
        Function: foo
        Parameter: x,y,z
        Body:
        Var: b;
        EndBody.
        Function: main
        Body:
        Var: c;
        foo(1,2);
        EndBody.
        """
        expect = str(TypeMismatchInStatement(CallStmt(Id("foo"),[IntLiteral(1),IntLiteral(2)])))
        self.assertTrue(TestChecker.test(input,expect,435))

    def test_undeclared_function36(self):
        """Simple program: main"""
        input = """
        Var: a;
        Function: foo
        Parameter: x,y,z
        Body:
        Var: b;
        x=1+2;
        EndBody.
        Function: main
        Body:
        Var: c;
        foo(1,2);
        EndBody.
        """
        expect = str(TypeMismatchInStatement(CallStmt(Id("foo"),[IntLiteral(1),IntLiteral(2)])))
        self.assertTrue(TestChecker.test(input,expect,436))

    def test_undeclared_function37(self):
        """Simple program: main"""
        input = """
        Var: a,d;
        Function: foo
        Parameter: x,y,z
        Body:
        Var: b;
        a=x+2;
        EndBody.
        Function: main
        Body:
        Var: c;
        foo(1,2,d);
        EndBody.
        """
        expect = str(TypeCannotBeInferred(CallStmt(Id("foo"),[IntLiteral(1),IntLiteral(2),Id("d")])))
        self.assertTrue(TestChecker.test(input,expect,437))

    def test_undeclared_function38(self):
        """Simple program: main"""
        input = """
        Var: a,d;
        Function: foo
        Parameter: x,y,z
        Body:
        Var: b;
        a=x+2;
        EndBody.
        Function: main
        Body:
        Var: c;
        foo(1,2,d);
        EndBody.
        """
        expect = str(TypeCannotBeInferred(CallStmt(Id("foo"),[IntLiteral(1),IntLiteral(2),Id("d")])))
        self.assertTrue(TestChecker.test(input,expect,438))

    def test_undeclared_function39(self):
        """Simple program: main"""
        input = """
        Var: a,d;
        Function: foo
        Parameter: x,y,z
        Body:
        Var: b;
        a=x+2;
        EndBody.
        Function: main
        Body:
        Var: c;
        foo(1,2,3);
        EndBody.
        """
        expect = str()
        self.assertTrue(TestChecker.test(input,expect,439))

    def test_undeclared_function40(self):
        """Simple program: main"""
        input = """
        Function: main
        Parameter: x,y,z
        Body:
        Var: b;
        Var: b;
        EndBody.
        """
        expect = str(Redeclared(Variable(),"b"))
        self.assertTrue(TestChecker.test(input,expect,440))

    def test_undeclared_function41(self):
        """Simple program: main"""
        input = """
        Function: main
        Parameter: x,y,z
        Body:
        Var: b;
        Var: b;
        EndBody.
        """
        expect = str(Redeclared(Variable(),"b"))
        self.assertTrue(TestChecker.test(input,expect,441))

    def test_undeclared_function41(self):
        """Simple program: main"""
        input = """
        Function: foo
        Parameter: y
        Body:
        Var: b = 1;
        b = y;
        Return;
        EndBody.
        Function: main
        Body:
        Var: x;
        x = foo("string");
        EndBody.
        """
        expect = str(TypeMismatchInStatement(Assign(Id("x"),CallExpr(Id("foo"),[StringLiteral("string")]))))
        self.assertTrue(TestChecker.test(input,expect,442))

    def test_undeclared_function(self):
        """Simple program: main"""
        input = """Var: b,c,a;
        Var: d,e,f,b;"""
        expect = str(Redeclared(Variable(),"b"))
        self.assertTrue(TestChecker.test(input,expect,443))

    def test_undeclared_function1(self):
        """Simple program: main"""
        input = """Var: a,b,c;
        Function: c
        Body:
        EndBody.
        """
        expect = str(Redeclared(Function(),"c"))
        self.assertTrue(TestChecker.test(input,expect,444))

    def test_undeclared_function2(self):
        """Simple program: main"""
        input = """Var: a,c;
        Function: main
        Body:
        Var: b;
        Var: e,b;
        EndBody.
        """
        expect = str(Redeclared(Variable(),"b"))
        self.assertTrue(TestChecker.test(input,expect,445))

    def test_undeclared_function3(self):
        """Simple program: main"""
        input = """Var: a,c;
        Function: main
        Parameter: a,x,y
        Body:
        Var: k,b;
        Var: e,b;
        EndBody.
        """
        expect = str(Redeclared(Variable(),"b"))
        self.assertTrue(TestChecker.test(input,expect,446))

    def test_undeclared_function4(self):
        """Simple program: main"""
        input = """Var: a,c;
        Function: main
        Parameter: a,x,y
        Body:
        Var: b;
        Var: e,b;
        EndBody.
        """
        expect = str(Redeclared(Variable(),"b"))
        self.assertTrue(TestChecker.test(input,expect,447))

    def test_undeclared_function5(self):
        """Simple program: main"""
        input = """Var: a,c;
        Function: main
        Parameter: a,x,y
        Body:
        Var: k,b;
        Var: a,b;
        EndBody.
        """
        expect = str(Redeclared(Variable(),"a"))
        self.assertTrue(TestChecker.test(input,expect,448))

    def test_undeclared_function5(self):
        """Simple program: main"""
        input = """
        Var: y;
        Function: main
        Parameter: a,x
        Body:
        Var: y,x;
        EndBody.
        """
        expect = str(Redeclared(Variable(),"x"))
        self.assertTrue(TestChecker.test(input,expect,449))

    def test50(self):
        """Simple program: main"""
        input = """
        Function: foo
        Parameter: x
        Body:
        x = 1;
        EndBody.
        Function: main
        Body:
        Var: a,b=3;
        a = foo(2) + b;
        EndBody.
        """
        expect = str()
        self.assertTrue(TestChecker.test(input,expect,450))

    def test51(self):
        """Simple program: main"""
        input = """
        Function: foo
        Parameter: x
        Body:
        x = 1;
        EndBody.
        Function: main
        Body:
        Var: a,b=3;
        a = -foo(2) + b;
        EndBody.
        Function: go
        Parameter: m,n
        Body:
        EndBody.
        """
        expect = str()
        self.assertTrue(TestChecker.test(input,expect,451))

    def test52(self):
        """Simple program: main"""
        input = """
        Function: foo
        Parameter: x
        Body:
        x = 1;
        EndBody.
        Function: main
        Body:
        Var: a,b=3;
        a = -b + 1;
        EndBody.
        """
        expect = str()
        self.assertTrue(TestChecker.test(input,expect,452))

    def test53(self):
        """Simple program: main"""
        input = """
        Function: foo
        Parameter: x
        Body:
        x = 1;
        EndBody.
        Function: main
        Body:
        Var: a,b=3;
        a = -(b + 1);
        EndBody.
        """
        expect = str()
        self.assertTrue(TestChecker.test(input,expect,453))

    def test54(self):
        """Simple program: main"""
        input = """
        Function: main
        Body:
        EndBody.
        Function: main
        Body:
        EndBody.
        """
        expect = str(Redeclared(Function(),("main")))
        self.assertTrue(TestChecker.test(input,expect,454))

    def test55(self):
        """Simple program: main"""
        input = """
        Function: main
        Parameter: x,y,x
        Body:
        EndBody.
        """
        expect = str(Redeclared(Variable(),"x"))
        self.assertTrue(TestChecker.test(input,expect,455))

    def test56(self):
        """Simple program: main"""
        input = """
        
        Function: main
        Parameter: y
        Body:
        Var: a,b=3;
        a = -foo(y) + b;
        EndBody.
        Function: foo
        Parameter: x
        Body:
        x = 1;
        Return 1;
        EndBody.
        """
        expect = str(TypeCannotBeInferred(CallExpr(Id("foo"),[Id("y")])))
        self.assertTrue(TestChecker.test(input,expect,456))

    def test57(self):
        """Simple program: main"""
        input = """
        Var: b=False;
        Var: c;

        Function: foo
        Body:
        b = True;
        EndBody.

        Function: main
        Body:
        Var: c;
        c = !b;
        EndBody.

        """
        expect = str()
        self.assertTrue(TestChecker.test(input,expect,457))

    def test58(self):
        """Simple program: main"""
        input = """
        Function: main
        Body:
        Var: a;
        If a Then a=False;
        EndIf.
        EndBody.
        """
        expect = str()
        self.assertTrue(TestChecker.test(input,expect,458))

    def test59(self):
        """Simple program: main"""
        input = """
        Function: main
        Body:
        Var: a;
        If a+1 Then a=False;
        EndIf.
        EndBody.
        """
        expect = str(TypeMismatchInStatement(If([(BinaryOp("+",Id("a"),IntLiteral(1)),[],[Assign(Id("a"),BooleanLiteral("false"))])],([],[]))))
        self.assertTrue(TestChecker.test(input,expect,459))

    def test60(self):
        """Simple program: main"""
        input = """
        Function: main
        Body:
        Var: a;
        If a+1 Then a=False;
        EndIf.
        EndBody.
        """
        expect = str(TypeMismatchInStatement(If([(BinaryOp("+",Id("a"),IntLiteral(1)),[],[Assign(Id("a"),BooleanLiteral("false"))])],([],[]))))
        self.assertTrue(TestChecker.test(input,expect,460))

    def test61(self):
        """Simple program: main"""
        input = """
        Var: b = 10;
            Var: c;
            Var: e;
            Var: f,g;
            Function: foo
            Body:

            EndBody.

            Function: main
            Body:
            Var : b = 1.0;
            g = 1.0;
            f = b +. g + 1.0;
            EndBody.
        """
        expect = str(TypeMismatchInExpression(BinaryOp("+",BinaryOp("+.",Id("b"),Id("g")),FloatLiteral(1.0))))
        self.assertTrue(TestChecker.test(input,expect,461))

    def test62(self):
        """Simple program: main"""
        input = """
        Function: main
             Parameter: x, y ,z
             Body:
             y = x || (x>z);
             EndBody.
        """
        expect = str(TypeMismatchInExpression(BinaryOp(">",Id("x"),Id("z"))))
        self.assertTrue(TestChecker.test(input,expect,462))

    def test63(self):
        """Simple program: main"""
        input = """
        Function: main
             Parameter: x, y ,z
             Body:
             y = x + y;
             EndBody.
        """
        expect = str()
        self.assertTrue(TestChecker.test(input,expect,463))

    def test_undeclared_function64(self):
        """Simple program: main"""
        input = """
        Var: a[1][2][3]={1,"str",3.2,{1,2}};
        Function: main
        Body:
        EndBody.
        """
        expect = str()
        self.assertTrue(TestChecker.test(input,expect,464))

    def test_undeclared_function65(self):
        """Simple program: main"""
        input = """
        Var: a={1,"str",3.2,{1,2}};
        Function: main
        Body:
        EndBody.
        """
        expect = str()
        self.assertTrue(TestChecker.test(input,expect,465))

    def test_undeclared_function66(self):
        """Simple program: main"""
        input = """
        Function: main
        Body:
        foo();
        EndBody.
        Function: foo
        Body:
        EndBody.
        """
        expect = str()
        self.assertTrue(TestChecker.test(input,expect,466))

    def test_undeclared_function67(self):
        """Simple program: main"""
        input = """
        Var: a[3];
        Function: main
        Body:
        EndBody.
        """
        expect = str()
        self.assertTrue(TestChecker.test(input,expect,467))

    def test_while_stmt_06(self):
        input ="""
            Function: main
            Body:
                Var: a , b = 1;
                If b==1 Then
                a = a +. 0.5;
                ElseIf b!=1 Then
                a = True;
                EndIf.
                a = a - 1;
            EndBody.

        """
        expect = str(TypeMismatchInStatement(Assign(Id("a"),BooleanLiteral("true"))))
        self.assertTrue(TestChecker.test(input,expect,468))

    def test_while_stmt_07(self):
        input ="""
            Function: main
            Body:
                Var: a , b = 1;
                If b==1 Then
                a = a +. 0.5;
                ElseIf b!=1 Then
                a = 0.2;
                Else
                Var: c=3;
                a = a + 1;
                EndIf.
                a = a - 1;
            EndBody.

        """
        expect = str(TypeMismatchInExpression(BinaryOp("+",Id("a"),IntLiteral(1))))
        self.assertTrue(TestChecker.test(input,expect,469))

    def test_while_stmt_08(self):
        input ="""
            Function: main
            Body:
            foo(2);
            EndBody.
            Function: foo
            Parameter: x
            Body:
            x = x + 1;
            EndBody.

        """
        expect = str()
        self.assertTrue(TestChecker.test(input,expect,470))

    def test_while_stmt_09(self):
        input ="""

            Function: foo
            Parameter: x
            Body:
            x = x + 1;
            EndBody.
            Function: main
            Body:
            foo(2);
            EndBody.
        """
        expect = str()
        self.assertTrue(TestChecker.test(input,expect,471))

    def test_while_stmt_10(self):
        input ="""
            Function: foo
            Parameter: x
            Body:
            x = x + 1;
            EndBody.
            Function: main
            Body:
            Var: a;
            a = foo(2) + 1;
            EndBody.
        """
        expect = str()
        self.assertTrue(TestChecker.test(input,expect,472))

    def test_while_stmt_11(self):
        input ="""
            Function: foo
            Parameter: x
            Body:
            x = x + 1;
            Return 1;
            EndBody.
            Function: main
            Body:
            Var: a = 2;
            a = foo(2)+1;
            EndBody.
        """
        expect = str()
        self.assertTrue(TestChecker.test(input,expect,473))

    def test_while_stmt_12(self):
        input ="""
            Var: a[3] = {1,2,3};
            Funtion: main
            Body:
            EndBody.
        """
        expect = str()
        self.assertTrue(TestChecker.test(input,expect,474))