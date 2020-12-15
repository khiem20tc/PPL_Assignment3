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

    def test_406(self):
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

    def testcase407(self):
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

    def testcase408(self):
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

    def testcase409(self):
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

    def testcase410(self):
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

    def testcase411(self):
        """Simple program: main"""
        input = """Var: a,b;
        Function: x
        Body:
        EndBody.
        """
        expect = str(NoEntryPoint())
        self.assertTrue(TestChecker.test(input,expect,411))

    def testcase412(self):
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

    def testcase413(self):
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

    def testcase414(self):
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

    def testcase415(self):
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

    def testcase416(self):
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

    def testcase417(self):
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

    def testcase418(self):
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

    def testcase419(self):
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

    def testcase420(self):
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

    def testcase421(self):
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

    def testcase422(self):
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

    def testcase423(self):
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

    def testcase424(self):
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

    def testcase425(self):
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

    def testcase426(self):
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

    def testcase427(self):
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

    def testcase428(self):
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

    def testcase429(self):
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

    def testcase430(self):
        """Simple program: main"""
        input = """
        Var: a[3]={1,2,3};
        Function: main
        Body:
        EndBody.
        """
        expect = str()
        self.assertTrue(TestChecker.test(input,expect,430))

    def testcase431(self):
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

    def testcase432(self):
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

    def testcase433(self):
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

    def testcase434(self):
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

    def testcase435(self):
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

    def testcase436(self):
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
        c = foo(1,2);
        EndBody.
        """
        expect = str(TypeMismatchInExpression(CallExpr(Id("foo"),[IntLiteral(1),IntLiteral(2)])))
        self.assertTrue(TestChecker.test(input,expect,436))

    def testcase437(self):
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

    def testcase438(self):
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

    def testcase439(self):
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

    def testcase440(self):
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

    def testcase441(self):
        """Simple program: main"""
        input = """
        Var: b, b;
        Function: main
        Parameter: x,y,z
        Body:
        Var: b;
        EndBody.
        """
        expect = str(Redeclared(Variable(),"b"))
        self.assertTrue(TestChecker.test(input,expect,441))

    def testcase442(self):
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
        expect = str(TypeMismatchInExpression(CallExpr(Id("foo"),[StringLiteral("string")])))
        self.assertTrue(TestChecker.test(input,expect,442))

    def testcase443(self):
        """Simple program: main"""
        input = """Var: b,c,a;
        Var: d,e,f,b;"""
        expect = str(Redeclared(Variable(),"b"))
        self.assertTrue(TestChecker.test(input,expect,443))

    def testcase443(self):
        """Simple program: main"""
        input = """Var: a,b,c;
        Function: c
        Body:
        EndBody.
        """
        expect = str(Redeclared(Function(),"c"))
        self.assertTrue(TestChecker.test(input,expect,444))

    def testcase445(self):
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

    def testcase446(self):
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

    def testcase447(self):
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

    def testcase448(self):
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

    def testcase449(self):
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

    def testcase450(self):
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

    def testcase451(self):
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

    def testcase452(self):
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

    def testcase453 (self):
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

    def testcase454(self):
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

    def testcase455(self):
        """Created automatically"""
        input = """
        Var: n;
        Function: fact
        Parameter: agjksabkbjk
        Body:
            If n == 0 Then
                Return 1;
            ElseIf (n>0) Then
                Return n * fact (n - 1);
            Else
                Return n;
            EndIf.
        EndBody.
        Function: main
        Body:
        EndBody."""
        expect = str()
        self.assertTrue(TestChecker.test(input,expect,455))

    def testcase456(self):
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

    def testcase457(self):
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

    def testcase458(self):
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

    def testcase459(self):
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

    def testcase460(self):
        """Simple program: main"""
        input = """
            Var: a;
            Function: foo
            Parameter: a,b
            Body:
                a = 10.0;
                b = 10.0;
                **Var: a = 10;**
                **x = a  + main() + foo1();**
                Return 1.0;
            EndBody.
            
            Function: foo1
            Body:
                Var: a = 10;
                a = foo(1.0,2.0);
                Return "string";
            EndBody.

            Function: main
            Parameter: a,b,c
            Body:
            
                Return 1;
            EndBody.
            
            """
        expect = str(TypeMismatchInStatement(Assign(Id('a'),CallExpr(Id('foo'),[FloatLiteral(1.0),FloatLiteral(2.0)]))))
        self.assertTrue(TestChecker.test(input, expect, 460))

    def testcase461(self):
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

    def testcase462(self):
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

    def testcase463(self):
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

    def testcase464(self):
        input ="""
            Function: main
            Body:
                Var: x = 1,i;
                For(i=2, i < x ,x) Do
                    Var: z = 1.1;
                    For(i=3,i<10,i) Do
                        z= 1.2 +. 1.0;
                        For(i=4,i<100,i+1) Do
                            z = True;
                            If x == 1 Then
                                i = x;
                            Else
                                i = -x;
                            EndIf.
                        EndFor.
                    EndFor.
                EndFor.
            EndBody.
        """
        expect = str(TypeMismatchInStatement(Assign(Id("z"),BooleanLiteral("true"))))
        self.assertTrue(TestChecker.test(input,expect,464))

    def testcase465(self):
        input ="""
            Function: main
            Body: 
                Var: a , b = 1, i = 1;
                For (i=1, i<10, a\\2) Do
                Var: c;
                a = a + 1;
                EndFor.
                a = a -. 0.5;
            EndBody.
            Function: foo
            Parameter: x
            Body:
            EndBody.

        """
        expect = str(TypeMismatchInExpression(BinaryOp("-.",Id("a"),FloatLiteral(0.5))))
        self.assertTrue(TestChecker.test(input,expect,465))

    def testcase466(self):
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

    def testcase467(self):
        """Simple program: main"""
        input = """
        Var: a[3];
        Function: main
        Body:
        EndBody.
        """
        expect = str()
        self.assertTrue(TestChecker.test(input,expect,467))

    def testcase468(self):
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

    def testcase469(self):
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

    def testcase470(self):
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

    def testcase471(self):
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

    def testcase472(self):
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

    def testcase473(self):
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

    def testcase474(self):
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
        self.assertTrue(TestChecker.test(input,expect,474))

    def testcase475(self):
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
        self.assertTrue(TestChecker.test(input,expect,475))

    def testcase476(self):
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
        self.assertTrue(TestChecker.test(input,expect,476))

    def testcase477(self):
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
        self.assertTrue(TestChecker.test(input,expect,477))

    def testcase478(self):
        input = """
        Var: s, arr;
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
            EndIf.
            Return;
        EndBody.
        Function: main
        Body:
            Var: m1, m2;
            arr = s;
            m1 = s;
            m2 = arr;
            Return 0;
        EndBody. """
        expect = str()
        self.assertTrue(TestChecker.test(input,expect,478))

    def testcase479(self):
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
        self.assertTrue(TestChecker.test(input,expect,479))

    def testcase480(self):
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
            Return;
        EndBody.
        """
        expect = str()
        self.assertTrue(TestChecker.test(input,expect,480))

    def testcase481(self):
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
        self.assertTrue(TestChecker.test(input,expect,481))

    def testcase482(self):
        input = """
        Var: abc = "string";
        Function: main
        Parameter: x
        Body:
            Var: athos = 500, pothos = 900, jerry, tom = 200;
            If (pothos - athos) < 400 Then jerry = pothos - tom;
            Else jerry = athos - tom;
            EndIf.
            Return x + abc;
        EndBody.
        Function: go
        Body:
        Var: a;
        a = main(2) +1;
        EndBody.
        """
        expect = str(TypeMismatchInExpression(BinaryOp("+",Id("x"),Id("abc"))))
        self.assertTrue(TestChecker.test(input,expect,482))

    def testcase483(self):
        input = """
        Var: abc = "string";
        Function: main
        Parameter: x
        Body:
            Var: athos = 500, pothos = 900, jerry, tom = 200;
            If (pothos - athos) < 400 Then jerry = pothos - tom;
            Else jerry = athos - tom;
            EndIf.
            Return abc;
        EndBody.
        Function: go
        Body:
        Var: a;
        a = main(2);
        EndBody.
        """
        expect = str()
        self.assertTrue(TestChecker.test(input,expect,483))

    def testcase484(self):
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
        self.assertTrue(TestChecker.test(input,expect,484))

    def testcase485(self):
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
        self.assertTrue(TestChecker.test(input,expect,485))

    def testcase486(self):
        """Created automatically"""
        input = """
        Function: main
        Body:
        Var: i = 0, a;
            For (i = 0, i < 10, 2) Do
                a= int_of_float(float_of_string(read()));
                Return a;
            EndFor.
        EndBody."""
        expect = str()
        self.assertTrue(TestChecker.test(input,expect,486))

    def testcase487(self):
        """Created automatically"""
        input = """
        Var: i=0, k=100;
        Function: main
        Body:
            For (i=12, i < k, i*i) Do
            goo();
            EndFor.
        EndBody."""
        expect = str(Undeclared(Function(),"goo"))
        self.assertTrue(TestChecker.test(input,expect,487))
        
    def testcase488(self):
        """Created automatically"""
        input = """
        Function: main
        Body:
        Var: i , x;
            For (i = 1, i <= x*x,i*i+.1.5)
            Do x=x+1;
            EndFor.
        EndBody."""
        expect = str(TypeMismatchInExpression(BinaryOp("+.",BinaryOp("*",Id("i"),Id("i")),FloatLiteral(1.5))))
        self.assertTrue(TestChecker.test(input,expect,488))
        
    def testcase489(self):
        """Created automatically"""
        input = """Function: main
        Body:
        Var:i=0;
            For (i=0, i!=9, (i*.2.0)) Do
                If i>=10 Then Break;
                EndIf.
            EndFor.
        EndBody."""
        expect = str(TypeMismatchInExpression(BinaryOp("*.",Id("i"),FloatLiteral(2.0))))
        self.assertTrue(TestChecker.test(input,expect,489))

    def testcase490(self):
        """Created automatically"""
        input = """
        Function: foo
        Body:
            Var: c="hihi";
            Return c;
        EndBody.
        Function: main 
        Body:
        Var: i;
            For (i=0, i!=9, i) Do
                If i==10 Then Continue;
                EndIf.
                foo(1);
            EndFor.
        EndBody."""
        expect = str(TypeMismatchInStatement(CallStmt(Id("foo"),[IntLiteral(1)])))
        self.assertTrue(TestChecker.test(input,expect,490))

    def testcase491(self):
        """Created automatically"""
        input = """
        Var: x;
        Function: main
            Parameter: j, brr[1000]
            Body:
                Var: x=0,i;
                For (i=0,True,i) Do
                    Var:x=1;
                    Do
                        Var:x=2;
                    While1==0
                    EndDo.
                    IfTrueThen
                        Var:x=3;
                    EndIf.
                EndFor.
            EndBody."""
        expect = str()
        self.assertTrue(TestChecker.test(input,expect,491))
    
    def testcase492(self):
        """Created automatically"""
        input = """Function: main
        Parameter: n
        Body:
        Var:factorial=1;
        print("Enter integer: ");
        read();
        For (i=0, i<=n, 1) Do
            factorial=factorial*i;
        EndFor.
        printStrLn(string_of_int(factorial));
        Return factorial;
        EndBody."""
        expect = str(TypeMismatchInStatement(CallStmt(Id("read"),[])))
        self.assertTrue(TestChecker.test(input,expect,492))

    def testcase493(self):
        """Simple program: main"""
        input = """
            Var: a;
            Function: foo
            Parameter: a,b
            Body:
                a = 10;
                b = 10.0;
                **Var: a = 10;**
                **x = a  + main() + foo1();**
                main(1,2,"string");
                Return 1;
            EndBody.
            
            Function: main
            Parameter: a,b,c
            Body:
            
                foo(1,2);
                Return ;
            EndBody.
            
            """
        expect = str(TypeMismatchInStatement(CallStmt(Id('foo'),[IntLiteral(1),IntLiteral(2)])))
        self.assertTrue(TestChecker.test(input, expect, 493))
    
    def testcase494(self):
        """Simple program: main"""
        input = """
            Var: a;
            Function: foo
            Parameter: a,b
            Body:
                a = 10;
                b = 10.0;
                **Var: a = 10;**
                **x = a  + main() + foo1();**
                a = 1 + main(1,2,"string") + foo1();
                Return 1;
            EndBody.
            
            Function: foo1
            Body:
                Return "string";
            EndBody.

            Function: main
            Parameter: a,b,c
            Body:
                a = a + 1;
                foo(1,2.0);
                Return 1;
            EndBody.
            
            """
        expect = str(TypeMismatchInStatement(Return(StringLiteral('string'))))
        self.assertTrue(TestChecker.test(input, expect, 494))
    
    def testcase495(self):
        """Simple program: main"""
        input = """
            Var: a;
            Function: foo
            Parameter: a,b
            Body:
                a = 10.0;
                b = 10.0;
                **Var: a = 10;**
                **x = a  + main() + foo1();**
                a = 1 + main(1,2,"string") + foo1();
                Return 1;
            EndBody.
            
            Function: foo1
            Body:
                Return "string";
            EndBody.

            Function: main
            Parameter: a,b,c
            Body:
            
                foo(1,2.0);
                Return 1;
            EndBody.
            
            """
        expect = str(TypeMismatchInStatement(Assign(Id('a'),BinaryOp('+',BinaryOp('+',IntLiteral(1),CallExpr(Id('main'),[IntLiteral(1),IntLiteral(2),StringLiteral("string")])),CallExpr(Id('foo1'),[])))))
        self.assertTrue(TestChecker.test(input, expect, 495))
    
    def testcase496(self):
        """Simple program: main"""
        input = """
            Var: a;
            Function: foo
            Parameter: a,b
            Body:
                a = 10.0;
                b = 10.0;
                **Var: a = 10;**
                **x = a  + main() + foo1();**
                Return 1.0;
            EndBody.
            
            Function: foo1
            Body:
                Var: a = 10;
                a = foo(1.0,2.0);
                Return "string";
            EndBody.

            Function: main
            Parameter: a,b,c
            Body:
            
                Return 1;
            EndBody.
            
            """
        expect = str(TypeMismatchInStatement(Assign(Id('a'),CallExpr(Id('foo'),[FloatLiteral(1.0),FloatLiteral(2.0)]))))
        self.assertTrue(TestChecker.test(input, expect, 496))
    
    def testcase497(self):
        """Simple program: main"""
        input = """
            Var: a;
            Function: foo
            Parameter: a,b
            Body:
                a = 10.0;
                b = 10.0;
                Return ;
            EndBody.
            
            Function: foo1
            Body:
                Var: a ;
                a = foo(1.0,2.0);
                Return "string";
            EndBody.

            Function: main
            Parameter: a,b,c
            Body:
            
                Return 1;
            EndBody.
            
            """
        expect = str(TypeMismatchInStatement(Assign(Id('a'),CallExpr(Id('foo'),[FloatLiteral(1.0),FloatLiteral(2.0)]))))
        self.assertTrue(TestChecker.test(input, expect, 497))

    def testcase498(self):
        """Simple program: main"""
        input = """
            Var: b = 10;
            Var: c;
            Var: e;
            Var: f,g;
            Function: foo
            Body:
                **b =  e =/= c;**
                c = !e;
            EndBody.
            
            Function: main
            Body:
            Var : b = 1.0;
            g = 1.0;
            **f = b +. g + 1.0;**
            f = 10.0 + 10;
            EndBody.
            
            """
        expect = str(TypeMismatchInExpression(BinaryOp('+',FloatLiteral(10.0),IntLiteral(10))))
        self.assertTrue(TestChecker.test(input, expect, 498))
    
    def testcase499(self):
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
        expect = str(TypeMismatchInExpression(BinaryOp('+',BinaryOp('+.',Id('b'),Id('g')),FloatLiteral(1.0))))
        self.assertTrue(TestChecker.test(input, expect, 499))
    
    def testcase500(self):
        """Simple program: main"""
        input = """
            
            Function: foo
            Parameter: a,b,c
            Body:
                main();
                foo1();
                foo2();

            EndBody.
            
            
            Function: foo1
            Body:
                Return 1;
            EndBody.
                
            
            Function: foo2
            Body:
            
            EndBody.
            
            Function: main
            Parameter: a, b, c
            Body:
                Return ;
            EndBody.
            
            """
        expect = str(TypeMismatchInStatement(CallStmt(Id('main'),[])))
        self.assertTrue(TestChecker.test(input, expect, 500))
    
    # def test_undeclared_var_13(self):
    #     """Simple program: main"""
    #     input = """
            
    #         Function: foo
    #         Parameter: a,b,c
    #         Body:
    #             a = 2;
    #             main();
    #             Return;
    #         EndBody.
            
            
    #         Function: foo1
    #         Parameter: d
    #         Body:
    #             d = 10;
    #             Return;
    #         EndBody.
                
            
    #         Function: foo2
    #         Body:
    #             Return;
    #         EndBody.
            
    #         Function: main
    #         Parameter: a, b, c
    #         Body:
    #             Return "str";
    #         EndBody.
            
    #         """
    #     expect = str(TypeMismatchInStatement(CallStmt(Id('main'),[])))
    #     self.assertTrue(TestChecker.test(input, expect, 413))
    
    # def test_undeclared_var_14(self):
    #     """Simple program: main"""
    #     input = """
            
    #         Function: foo
    #         Parameter: a,b,c
    #         Body:
    #             a = 2;
                
    #             foo1(1,2,"das");
    #             main(2,3,1.0);
    #             Return;
    #         EndBody.
            
            
    #         Function: foo1
    #         Parameter: d, c, e
    #         Body:
    #             d = 10;
    #             Return;
    #         EndBody.
                
            
    #         Function: foo2
    #         Body:
    #             Return;
    #         EndBody.
            
    #         Function: main
    #         Parameter: a, b, c
    #         Body:
    #             a = 10.1;
    #             Return ;
    #         EndBody.
            
    #         """
    #     expect = str(TypeMismatchInStatement(Assign(Id('a'),FloatLiteral(10.1))))
    #     self.assertTrue(TestChecker.test(input, expect, 414))