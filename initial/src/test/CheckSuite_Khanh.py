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

    def test_stupid_06(self):
        input ="""
            Function: main
            Body:
                Var:x;
                x = 1 + 2 + 3 + y ;
            EndBody.
        """
        expect = str(Undeclared(Identifier() , "y"))
        self.assertTrue(TestChecker.test(input,expect,406))
    
    def test_stupid_07(self):
        input = """
            Function: foo1
            Body:
                Return 1;
            EndBody.
            Function: foo2
            Body:
                Return 2;
            EndBody.
            Function: foo3
            Parameter: x,y,z[123]
            Body:
                Return 3;
            EndBody.
        """
        expect = str(NoEntryPoint())
        self.assertTrue(TestChecker.test(input,expect,407))

    def test_stupid_08(self):
        input = """
            Function: main
            Body:
                Var:x = 1,a;
                foo(x);
                a = foo_goo();
            EndBody.

            Function: foo
            Parameter: x
            Body:
                Return ;
            EndBody.
        """
        expect = str(Undeclared(Function() , "foo_goo"))
        self.assertTrue(TestChecker.test(input,expect,408))
    def test_stupid_09(self):
        input = """
            Function: main
            Body:
                Var:x = 1,a;
                foo(x);
            EndBody.

            Function: foo
            Parameter: x
            Body:
                Return 1;
            EndBody.
        """
        expect = str(TypeMismatchInStatement(Return(IntLiteral(1))))
        self.assertTrue(TestChecker.test(input,expect,409))

#=========================================================================#
    def test_assign_01(self):
        input ="""
            Function: main
            Body:
                Var: x, y ,z;
                x = 1;
                y = 2;
                z = x + y + meow_meow;
            EndBody.

            Function: meow_meow
            Body:
                Return 1;
            EndBody.
        """
        expect = str(Undeclared(Identifier(), "meow_meow"))
        self.assertTrue(TestChecker.test(input,expect,410))
    
    def test_assign_02(self):
        input ="""
            Function: foo
            Body:
                Return 1;
            EndBody.
            Function: main
            Body:
                Var: x = 1, y[5] = {1,2,3,4,5};
                x = y;
            EndBody.
        """
        expect = str(TypeMismatchInStatement(Assign(Id("x"),Id("y"))))
        self.assertTrue(TestChecker.test(input,expect,411))
    
    def test_assign_03(self):
        input ="""
            Function: main
            Parameter: x , y[2]
            Body:
                y[1] = 1.1;
                y[2] = 1;
            EndBody.
        """
        expect = str(TypeMismatchInStatement(Assign(ArrayCell(Id("y"),[IntLiteral(2)]),IntLiteral(1))))
        self.assertTrue(TestChecker.test(input,expect,412))
    
    def test_assign_04(self):
        input ="""
            Function: foo
            Body:
                Return {1,2,3};
            EndBody.

            Function: main
            Body:
                Var: x[3];
                x = foo();
            EndBody.
        """
        expect = str()
        self.assertTrue(TestChecker.test(input,expect,413))
    
    def test_assign_05(self):
        input ="""
            Function: foo
            Parameter: x
            Body:
                Return 1;
            EndBody.

            Function: main
            Body:
                Var:x , y , z[5];
                x = 1 + foo(z[5]);
            EndBody.
        """
        expect = str(TypeCannotBeInferred(Assign(Id("x") , BinaryOp("+",IntLiteral(1),CallExpr(Id("foo"),[ArrayCell(Id("z"),[IntLiteral(5)])])))))
        self.assertTrue(TestChecker.test(input,expect,414))
    
    def test_assign_06(self):
        input ="""
            Function: foo
            Parameter: x
            Body:
                x = 2.2;
                Return 1;
            EndBody.

            Function: main
            Body:
                Var: a;
                a = foo(goo());
            EndBody.

            Function: goo
            Body:
                Return 2;
            EndBody.
        """
        expect = str(TypeMismatchInStatement(Return(IntLiteral(2))))
        self.assertTrue(TestChecker.test(input,expect,415))
    
    def test_assign_07(self):
        input ="""
            Function: foo
            Parameter: x[5]
            Body:
                Var: a;
                a = 1 + 2 + 3 + 4;
                Return ;
            EndBody.
            Function: main
            Body:
                Var:x ;
                x = foo(x);
            EndBody.
        """
        expect = str(TypeMismatchInExpression(CallExpr(Id("foo"),[Id("x")])))
        self.assertTrue(TestChecker.test(input,expect,416))
    
    def test_assign_08(self):
        input ="""
            Function: foo
            Body:
                Var: a[5];
                a  = {1,2,3,4,5};
                Return a;
            EndBody.
            Function: main
            Body:
                Var: x;
                x = foo()[1][2];
            EndBody.
        """
        expect = str(TypeMismatchInExpression(ArrayCell(CallExpr(Id("foo"),[]),[IntLiteral(1),IntLiteral(2)])))
        self.assertTrue(TestChecker.test(input,expect,417))
    
    def test_assign_09(self):
        input ="""
            Function: foo
            Body:
                Return 1;
            EndBody.
            Function: main
            Body:
                
                Var: x,y,z,t;
                t = -1;
                x = 1.1;
                y = foo();
                z = x + y;
            EndBody.
        """
        expect = str(TypeMismatchInExpression(BinaryOp("+",Id("x"),Id("y"))))
        self.assertTrue(TestChecker.test(input,expect,418))
    
    def test_assign_10(self):
        input ="""
        Function: foo
        Body:
            Return {1,2,3};
        EndBody.

        Function: main
        Body:
            Var: x[3],y;
            x = foo();
            y = x[1] +. 1.1;
        EndBody.
        """
        expect = str(TypeMismatchInExpression(BinaryOp("+.", ArrayCell(Id("x"),[IntLiteral(1)]) ,FloatLiteral(1.1))))
        self.assertTrue(TestChecker.test(input,expect,419))

#============================================================================#
    def test_if_stmt_01(self):
        input ="""
        Function: main
        Parameter: x,y
        Body:
            Var: a = 2;
            If(2) Then
                x = 1;
            EndIf.
            x = 1.1;
        EndBody.
        """
        expect = str(TypeMismatchInStatement(If([(IntLiteral(2),[],[Assign(Id("x"),IntLiteral(1))])], ([],[]) ) ))
        self.assertTrue(TestChecker.test(input,expect,420))

    def test_if_stmt_02(self):
        input ="""
            Function: main
            Body:
                Var: a = 2,x;
                Var: z[5] = {1,2,3,4,5};
                If(a == 2) Then
                    x = 1;
                ElseIf (a == 3) Then
                    x = 2;
                ElseIf (a == 3) Then
                    x = z[1];
                Else x = 2.1;
                EndIf.
            EndBody.
        """
        expect = str(TypeMismatchInStatement(Assign(Id("x"),FloatLiteral(2.1))))
        self.assertTrue(TestChecker.test(input,expect,421))
    def test_if_stmt_03(self):
        input ="""
        Function: main
        Body:
            Var: a = 2,x = 3 , y , meow_meow;
            Var: z[5] = {1,2,3,4,5};
            If(a == 2) Then
                If(x == 3) Then
                    y = 1;
                Else y = 2;
                EndIf.
            Else x[1] = meow_meow;
            EndIf.
        EndBody.
        """
        expect = str(TypeMismatchInExpression(ArrayCell(Id("x"),[IntLiteral(1)])))
        self.assertTrue(TestChecker.test(input,expect,422))
    def test_if_stmt_04(self):
        input ="""
            Function: foo
            Body:
                Return 1;
            EndBody.

            Function: goo
            Body:
                Return {1.1,2.2,3.3,4.4,5.5};
            EndBody.

            Function: main
            Body:
                Var: x = 1, y , z , t;
                If (x > foo()) Then
                    y = 2;
                Else
                    If (x <= foo()) Then
                        y = z;
                    Else
                        z = goo()[1];
                    EndIf.
                EndIf.
            EndBody.
        """
        expect = str(TypeMismatchInStatement(Assign(Id("z"),ArrayCell(CallExpr(Id("goo"),[]),[IntLiteral(1)]))))
        self.assertTrue(TestChecker.test(input,expect,423))
    def test_if_stmt_05(self):
        input ="""
            Var: a;
            Function: main
            Body:
                Var: x;
                If (x == 1) Then
                    a = 2;
                EndIf.
            EndBody.

            Function: foo
            Body:
                a = 1.1;
            EndBody.
        """
        expect = str(TypeMismatchInStatement(Assign(Id("a"),FloatLiteral(1.1))))
        self.assertTrue(TestChecker.test(input,expect,424))
    def test_if_stmt_06(self):
        input ="""
            Function: main
            Body:
                If (foo()) Then
                EndIf.
            EndBody.

            Function: foo
            Body:
                Return 1;
            EndBody.
        """
        expect = str(TypeMismatchInStatement(Return(IntLiteral(1))))
        self.assertTrue(TestChecker.test(input,expect,425))
    def test_if_stmt_07(self):
        input ="""
            Function: main
            Body:
                Var: x , y , z;
                If(x) Then
                    x = False;
                Else
                    y = x;
                    If(y) Then
                        z = y;
                    EndIf.
                EndIf.
                z = 1;
            EndBody.
        """
        expect = str(TypeMismatchInStatement(Assign(Id("z"),IntLiteral(1))))
        self.assertTrue(TestChecker.test(input,expect,426))
    def test_if_stmt_08(self):
        input ="""
            Function: main
            Body:
                Var: x , y , z;
                y = 0.5;
                z = y;
                z = 1;
            EndBody.
        """
        expect = str(TypeMismatchInStatement(Assign(Id("z"),IntLiteral(1))))
        self.assertTrue(TestChecker.test(input,expect,427))
    def test_if_stmt_08(self):
        input ="""
            Function: main
            Body:
                Var: x = False, y;
                If(x) Then
                    Var: x;
                    x = 1;
                ElseIf(x) Then
                    Var: x;
                    x = 1.1;
                    y = x;
                EndIf.
                y = 1;
            EndBody.
        """
        expect = str(TypeMismatchInStatement(Assign(Id("y"),IntLiteral(1))))
        self.assertTrue(TestChecker.test(input,expect,427))
    def test_if_stmt_09(self):
        input ="""
            Function: main
            Body:
                Var: x;
                If(x) Then
                    Var: y = True;
                    y = foo()[1];
                EndIf.
            EndBody.

            Function: foo
            Body:
                Return {1,2,3};
            EndBody.
        """
        expect = str(TypeCannotBeInferred(Assign(Id("y"),ArrayCell(CallExpr(Id("foo"),[]),[IntLiteral(1)]))))
        self.assertTrue(TestChecker.test(input,expect,428))
    def test_if_stmt_10(self):
        input ="""
        Function: main
        Parameter: x
        Body:
            Var: y , z;
            If(x) Then
                y = 1;
            EndIf.
            x = 1;
        EndBody.
        """
        expect = str(TypeMismatchInStatement(Assign(Id("x"),IntLiteral(1))))
        self.assertTrue(TestChecker.test(input,expect,429))
#==================================================================
    def test_for_stmt_1(self):
        input ="""
        Function: main
        Body:
            Var: x = 1;
            For(x = foo() , x < 1 , 1) Do 
            EndFor.
        EndBody.
        Function: foo
        Body:
            Return 1.1;
        EndBody.
        """
        expect = str(TypeMismatchInStatement(Return(FloatLiteral(1.1))))
        self.assertTrue(TestChecker.test(input,expect,430))
    def test_for_stmt_2(self):
        input ="""
        Function: main
        Body:
            Var:x = 1.1 , y , z;
            For (y = 1, y > (1+2+3) , 4 ) Do
                Var: x = 1;
                z = x;
                y = y + 1;
            EndFor.
            z = 1.2;
        EndBody.
        Function: foo
        Body:
            Return 1.1;
        EndBody.
        """
        expect = str(TypeMismatchInStatement(Assign(Id("z"),FloatLiteral(1.2))))
        self.assertTrue(TestChecker.test(input,expect,431))

    def test_for_stmt_3(self):
        input ="""
            Function: main
            Body:
                Var:x;
                For (x = 1, x == foo() , 1) Do
                    Var: y = 1;
                    If (x == 1) Then x = 2;
                    ElseIf(x==2) Then y = 1.1;
                    EndIf.
                EndFor.
            EndBody.
            Function: foo
            Body:
                Return 1;
            EndBody.
        """
        expect = str(TypeMismatchInStatement(Assign(Id("y"),FloatLiteral(1.1))))
        self.assertTrue(TestChecker.test(input,expect,432))
    def test_for_stmt_4(self):
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
        self.assertTrue(TestChecker.test(input,expect,433))
    def test_for_stmt_5(self):
        input ="""
            Function: main
            Body:
                Var: x = 1;
                For(x=2,x<=.1,x) Do
                    x = 123;
                EndFor.
            EndBody.
        """
        expect = str(TypeMismatchInExpression(BinaryOp("<=.",Id("x"),IntLiteral(1))))
        self.assertTrue(TestChecker.test(input,expect,434))
    def test_for_stmt_6(self):
        input ="""
            Function: swap
            Parameter: x , y
            Body:
                Var: z = 1,result[2];
                z = x;
                x = y;
                y = z;
                result[0] = y;
                result[1] = x;
                Return result;
            EndBody.
            Function: main
            Body:
                Var: i;
                For(i = 1, i < 10 , 1) Do
                    Var: b,c;
                    If i == 1 Then
                        Var: a[2];
                        a = swap(i,i+1);
                        b = a[0];
                        c = a[1];
                    EndIf.
                    b = "Hello Darkness my old friend";
                    **b = 1.1;**
                EndFor.

            EndBody.
        """
        expect = str(TypeMismatchInStatement(Assign(Id("b"),StringLiteral("Hello Darkness my old friend"))))
        self.assertTrue(TestChecker.test(input,expect,435))
    def test_for_stmt_7(self):
        input ="""
            Function: main
            Body:
                Var: z;
                z = foo();
            EndBody.

            Function: foo
            Body:
                If (1>=2) Then
                    Return 1;
                Else Return 2;
                EndIf.
            EndBody.
        """
        expect = str(TypeCannotBeInferred(Assign(Id("z"),CallExpr(Id("foo"),[]))))
        self.assertTrue(TestChecker.test(input,expect,436))
    def test_for_stmt_8(self):
        input ="""
            Function: main
            Body:
                Var: index = 1;
                For(index = 2, index <= 100, index) Do
                    Var: i = 1;
                    Var: i = 1.1;
                EndFor.
            EndBody.
        """
        expect = str(Redeclared(Variable(),"i"))
        self.assertTrue(TestChecker.test(input,expect,437))
    def test_for_stmt_9(self):
        input ="""
            Function: foo
            Body:
                Return 1;
            EndBody.

            Function: goo
            Body:
                Return 1.1;
            EndBody.

            Function: main
            Body:
                Var: x;
                For (x = 1, x == foo() , 1) Do
                    While x == 2 Do
                        Var: z;
                        x = foo();
                        Do 
                            z = goo();
                        While z <= 1
                        EndDo.                        
                    EndWhile.
                EndFor.
            EndBody.

        """
        expect = str(TypeMismatchInExpression(BinaryOp("<=",Id("z"),IntLiteral(1))))
        self.assertTrue(TestChecker.test(input,expect,438))
    def test_for_stmt_10(self):
        input ="""
            Function: main
            Body:
                Var: x = 1, y = 2;
                For(x = 1, x <= 10, x) Do
                    Var: y = 2.2, z;
                    For(x = 2, z , x) Do
                        z = 1;
                    EndFor.
                EndFor.
            EndBody.
        """
        expect = str(TypeMismatchInStatement(Assign(Id("z"),IntLiteral(1))))
        self.assertTrue(TestChecker.test(input,expect,439))
#==============================================================================
    def test_While_stmt_01(self):
        input ="""
            Function: foo
            Body:
                Return 1;
            EndBody.

            Function: main
            Body:
                Var: z , y  , x;
                While z >= foo() Do
                    Var: y;
                    y = 1;
                    x = y;
                EndWhile.
                If (y >=. 1.1) Then
                    z = foo();
                    Do x = "This is String";
                    While z >= foo()
                    EndDo.
                EndIf.
            EndBody.
        """
        expect = str(TypeMismatchInStatement(Assign(Id("x"),StringLiteral("This is String"))))
        self.assertTrue(TestChecker.test(input,expect,440))
    def test_while_stmt_02(self):
        input ="""
            Function: foo
            Body:
                Var: x = 1;
                If (x == 1) Then
                    Return 1.1;
                EndIf.
            EndBody.
            Function: main
            Body:
                Var: x;
                While(x =/= foo()) Do
                    x = foo();
                EndWhile.
                x = 1;
            EndBody.

        """
        expect = str(TypeMismatchInStatement(Assign(Id("x"),IntLiteral(1))))
        self.assertTrue(TestChecker.test(input,expect,441))
    def test_while_stmt_03(self):
        input ="""
            Function: main
            Body:
                Var: x = 1.0;
                While (x <=. 1.1) Do
                    Return;
                EndWhile.
                Return 1;
            EndBody.
        """
        expect = str(TypeMismatchInStatement(Return(IntLiteral(1))))
        self.assertTrue(TestChecker.test(input,expect,442))
    def test_while_stmt_04(self):
        input ="""
            Function: main
            Body:
                Var: x,y[3]={1.1,2.2,3.3},result;
                While x == 1 Do
                    Var: y;
                    If x == 1 Then
                        y = 1.1;
                    EndIf.
                    result = x;
                EndWhile.
                y[0] = result;
            EndBody.
        """
        expect = str(TypeMismatchInStatement(Assign(ArrayCell(Id("y"),[IntLiteral(0)]),Id("result"))))
        self.assertTrue(TestChecker.test(input,expect,443))
    def test_while_stmt_05(self):
        input ="""
            Function: findMaxInt
            Parameter: a[4]
            Body:
                Var: i = 0, result = 1;
                result = a[0];
                While(i <= 3) Do
                    If result < a[i] Then
                        result = a[i];
                    EndIf.
                    i = i + 1;
                EndWhile.
                Return result;
            EndBody.
            Function: main
            Body:
                Var: arr[4] = {1,2,3,4},result;
                result = findMaxInt(arr);
            EndBody.
        """
        expect = str()
        self.assertTrue(TestChecker.test(input,expect,444))
    def test_while_stmt_06(self):
        input ="""
            Function: main
            Body:
                Var: meow_meow;
                While(meow_meow) Do
                    meow_meow = 2;
                EndWhile.
            EndBody.

        """
        expect = str(TypeMismatchInStatement(Assign(Id("meow_meow"),IntLiteral(2))))
        self.assertTrue(TestChecker.test(input,expect,445))
    def test_while_stmt_07(self):
        input ="""
            Var: a;
            Function: attack
            Parameter: x,y
            Body:
                a=x+2;
                y = 1;
                While(meow_meow) Do
                    Var: meow_meow;
                    meow_meow = 2;
                EndWhile.
            EndBody.
            Function: main
            Body:
                Var: hpPotter = 100, hpVoldermort = 1000;
                attack(hpPotter, hpVoldermort);
            EndBody.
            Function: test
            Parameter: a , b
            Body:
            a = 1; 
            b = 2;
            EndBody.
        """
        expect = str()
        self.assertTrue(TestChecker.test(input,expect,446))
    def test_while_stmt_08(self):
        input ="""
            Function: calculator
            Parameter: x
            Body:
                If (x > 1) Then
                    Return x;
                Else
                    While x > 1 Do
                        x = x - 1;
                    EndWhile.
                EndIf.
            EndBody.

            Function: main
            Body:
                Var: x = 10.0 , result;
                result = calculator(x);
            EndBody.
        """
        expect = str(TypeMismatchInExpression(CallExpr(Id("calculator"),[Id("x")])))
        self.assertTrue(TestChecker.test(input,expect,447))
    def test_while_stmt_09(self):
        input ="""
            Function: main
            Body:
                Var: result;
                While(result == 1) Do
                    result = result -1;
                EndWhile.
                result = this_is_function();
            EndBody.
            Function: this_is_function
            Body:
                Var: string = "This is string";
                Return string;
            EndBody.
        """
        expect = str(TypeMismatchInStatement(Return(Id("string"))))
        self.assertTrue(TestChecker.test(input,expect,448))
    def test_while_stmt_10(self):
        input ="""
            Var: x;
            Function: main
            Body:
            Var: y,z;
                x = 1;
                While x >= 2 Do
                    Var:x = 2.2,result;
                    If x =/= 2.2 Then
                        result = "Some thing went wrong!";
                    EndIf.
                    x = x + 1;
                EndWhile.
            EndBody.
        """
        expect = str(TypeMismatchInExpression(BinaryOp("+",Id("x"),IntLiteral(1))))
        self.assertTrue(TestChecker.test(input,expect,449))
#==============================================================================
    # def test_do_while_stmt_02(self):
    #     input ="""
    #     """
    #     expect = str()
    #     self.assertTrue(TestChecker.test(input,expect,451))
    # def test_do_while_stmt_03(self):
    #     input ="""
    #     """
    #     expect = str()
    #     self.assertTrue(TestChecker.test(input,expect,452))
    # def test_do_while_stmt_04(self):
    #     input ="""
    #     """
    #     expect = str()
    #     self.assertTrue(TestChecker.test(input,expect,453))
    # def test_do_while_stmt_05(self):
    #     input ="""
    #     """
    #     expect = str()
    #     self.assertTrue(TestChecker.test(input,expect,454))
    # def test_do_while_stmt_06(self):
    #     input ="""
    #     """
    #     expect = str()
    #     self.assertTrue(TestChecker.test(input,expect,455))
    # def test_do_while_stmt_07(self):
    #     input ="""
    #     """
    #     expect = str()
    #     self.assertTrue(TestChecker.test(input,expect,456))
    # def test_do_while_stmt_08(self):
    #     input ="""
    #     """
    #     expect = str()
    #     self.assertTrue(TestChecker.test(input,expect,457))
    # def test_do_while_stmt_09(self):
    #     input ="""
    #     """
    #     expect = str()
    #     self.assertTrue(TestChecker.test(input,expect,458))
    # def test_do_while_stmt_10(self):
    #     input ="""
    #     """
    #     expect = str()
    #     self.assertTrue(TestChecker.test(input,expect,459))





#==============================================================================




























# import unittest
# from TestUtils import TestChecker
# from StaticError import *
# from AST import *

# class CheckSuite(unittest.TestCase):


# #==========================declare main in main function?============================================= 
#     # Test valid var declare
#     def test_valid_declare_variable(self):
#         """Simple program: main"""
#         input = """
#         Var: x, y, z;
#         Function: main
#             Body:
#                 Var: x, y, z, main;
#                 Return;
#             EndBody."""
#         expect = str("")
#         self.assertTrue(TestChecker.test(input,expect,413)) 


#     # Test valid param declare
#     def test_valid_declare_parameter(self):
#         """Simple program: main"""
#         input = """Var: x, y, z;
#         Function: main
#             Parameter: x, y, z, main
#             Body:
#                 Return;
#             EndBody."""
#         expect = str("")
#         self.assertTrue(TestChecker.test(input,expect,415))
    
# #============================================================================== 


# #============================================================================== 
#     def test_voidtype_in_assign(self):
#         """Simple program: main"""
#         input = """
#         Var: x;
#         Function: main
#             Body:
#                 foo(1);
#                 x = foo(1);
#                 Return;
#             EndBody.
#         Function: foo
#             Parameter: x
#             Body:
#                 Return;
#             EndBody."""
#         expect = str(TypeMismatchInStatement(Assign(Id("x"), CallExpr(Id("foo"), [IntLiteral(1)]))))
#         self.assertTrue(TestChecker.test(input,expect,443))

#     def test_voidtype_in_expression(self):
#         """Simple program: main"""
#         input = """
#         Var: x;
#         Function: main
#             Body:
#                 foo(1);
#                 x = foo(1) + 2;
#                 Return;
#             EndBody.
#         Function: foo
#             Parameter: x
#             Body:
#                 Return;
#             EndBody."""
#         expect = str(TypeMismatchInExpression(BinaryOp("+", CallExpr(Id("foo"), [IntLiteral(1)]), IntLiteral(2))))
#         self.assertTrue(TestChecker.test(input,expect,444))

#     def test_voidtype_in_funccall(self):
#         """Simple program: main"""
#         input = """
#         Var: x;
#         Function: main
#             Body:
#                 foo(1);
#                 foo(foo(10));
#                 Return;
#             EndBody.
#         Function: foo
#             Parameter: x
#             Body:
#                 Return;
#             EndBody."""
#         expect = str(TypeMismatchInStatement(CallStmt(Id("foo"), [CallExpr(Id("foo"), [IntLiteral(10)])])))
#         self.assertTrue(TestChecker.test(input,expect,445))


#     def test_returntype_8(self):
#         """Simple program: main"""
#         input = """
#         Var: x;
#         Function: foo
#             Parameter: x[3]
#             Body:
#                 Return;
#             EndBody.
#         Function: main
#             Body:
#                 Return foo({1,2,3});
#             EndBody."""
#         expect = str(TypeMismatchInStatement(Return(CallExpr(Id("foo"), [ArrayLiteral([IntLiteral(1), IntLiteral(2), IntLiteral(3)])]))))
#         self.assertTrue(TestChecker.test(input,expect,453))



# #================================================================
#     def test_assign_1(self):
#         """Simple program: main"""
#         input = """
#         Var: x;
#         Function: main
#             Body:
#                 x = x + foo(x);
#                 Return;
#             EndBody.
#         Function: foo
#             Parameter: x
#             Body:
#                 Return 1;
#             EndBody."""
#         expect = str("")
#         self.assertTrue(TestChecker.test(input,expect,454))

#     def test_assign_5(self):
#         """Simple program: main"""
#         input = """
#         Function: main
#             Body:
#                 Var: x[5] = {1.1, 2.2, 3.3, 4.4, 5.5}, y[5] = {1,2,3,4,5};
#                 y = foo(1);
#                 foo(2)[0] = x[3];
#                 Return;
#             EndBody.
#         Function: foo
#             Parameter: x
#             Body:
#                 Return {5,4,3,2,1};
#             EndBody.
#             """
#         expect = str(TypeMismatchInStatement(Assign(ArrayCell(CallExpr(Id("foo"), [IntLiteral(2)]), [IntLiteral(0)]), ArrayCell(Id("x"), [IntLiteral(3)]))))
#         self.assertTrue(TestChecker.test(input,expect,458))


#     def test_assign_6(self):
#         """Simple program: main"""
#         input = """
#         Var: x[5];
#         Function: main
#             Body:
#                 Var: y[5] = {1,2,3,4,5};
#                 x = {1.1, 2.2, 3.3, 4.4, 5.5};
#                 y = foo(1);
#                 foo(y[4] + 2)[0] = y[0] + 1;
#                 Return;
#             EndBody.
#         Function: foo
#             Parameter: y
#             Body:
#                 y = x[1];
#                 Return {5,4,3,2,1};
#             EndBody.
#             """
#         expect = str(TypeMismatchInStatement(Assign(Id("y"), ArrayCell(Id("x"), [IntLiteral(1)]))))
#         self.assertTrue(TestChecker.test(input,expect,459))


#     def test_function_call_1(self):
#         """Simple program: main"""
#         input = """
#         Var: x[2][2] = {{1.1, 2.2},{3.3, 4.4}};
#         Function: main
#             Body:
#                 x = foo(x);
#                 Return;
#             EndBody.
#         Function: foo
#             Parameter: y[2][2]
#             Body:
#                 Return {{1,2},{3,4}};
#             EndBody.
#             """
#         expect = str(TypeMismatchInStatement(Return(ArrayLiteral([ArrayLiteral([IntLiteral(1),IntLiteral(2)]),ArrayLiteral([IntLiteral(3),IntLiteral(4)])]))))
#         self.assertTrue(TestChecker.test(input,expect,462))


#     def test_function_call_7(self):
#         """Simple program: main"""
#         input = """
#         Function: foo
#             Parameter: x
#             Body:
#                 x = 1;
#                 Return {0};
#             EndBody.
#         Function: main
#             Body:
#                 foo(goo(1)[0])[0] = foo(1)[1];
#                 Return;
#             EndBody.
#         Function: goo
#             Parameter: x
#             Body:
#                 Return {0};
#             EndBody."""
#         expect = str(TypeCannotBeInferred(Assign(    ArrayCell(CallExpr(Id("foo"), [ArrayCell(CallExpr(Id("goo"), [IntLiteral(1)]), [IntLiteral(0)])]), [IntLiteral(0)]),      ArrayCell(CallExpr(Id("foo"), [IntLiteral(1)]), [IntLiteral(1)])     )))
#         self.assertTrue(TestChecker.test(input,expect,468))



#     def test_function_call_12(self):
#         """Simple program: main"""
#         input = """
#         Function: foo
#             Parameter: x, y
#             Body:
#                 Var: z;
#                 z = foo(y+1, foo(x, 1.1));
#                 Return z;
#             EndBody.
#         Function: main
#             Body:
#                 Return;
#             EndBody."""
#         expect = str(TypeMismatchInExpression(CallExpr(Id("foo"), [Id("x"), FloatLiteral(1.1)])))
#         self.assertTrue(TestChecker.test(input,expect,473))

#     def test_function_call_13(self):
#         """Simple program: main"""
#         input = """
#         Function: foo
#             Parameter: x, y
#             Body:
#                 Var: z;
#                 z = foo( float_of_int(y) +. foo(1.1, 1.1) , int_of_float(foo(x, 1)) );
#                 Return z;
#             EndBody.
#         Function: main
#             Body:
#                 Return;
#             EndBody."""
#         expect = str(TypeMismatchInExpression(CallExpr(Id("foo"), [FloatLiteral(1.1), FloatLiteral(1.1)])))
#         self.assertTrue(TestChecker.test(input,expect,474))


#     def test_arraycell_5(self):
#         """Simple program: main"""
#         input = """
#         Function: foo
#             Parameter: x[2][3], y
#             Body:
#                 x[x[0][y]][foo(x, foo(x, y))] = 1.1;
#                 Return 1;
#             EndBody.
#         Function: main
#             Body:
#                 Return foo({{1,2,3},{4,5,6}});
#             EndBody."""
#         expect = str(TypeMismatchInStatement(Assign(ArrayCell(Id("x"), [ArrayCell(Id("x"), [IntLiteral(0), Id("y")]), CallExpr(Id("foo"), [Id("x"), CallExpr(Id("foo"), [Id("x"), Id("y")])])]), FloatLiteral(1.1))))
#         self.assertTrue(TestChecker.test(input,expect,489)) 

#     def test_valid_program_4(self):
#         input = """
#         Function: sqrt
#             Parameter: x
#             Body:
#                 Return 1.1;
#             EndBody.
#         Function: radius
#             Parameter: x, y
#             Body:
#                 Var: radius;
#                 radius = sqrt(x*.x +. y*.y);
#                 Return radius;
#             EndBody.
#         Function: main
#             Body:
#                 Var : x = 3.5e0, y = 4.6e-0;
#                 printStrLn(string_of_float(radius(x, y)));
#                 Return;
#             EndBody."""
#         expect = str("")
#         self.assertTrue(TestChecker.test(input,expect,493))


#     def test_valid_program_5(self):
#         input = """Var: x[5] = {1,2,3,4,5};
#         Function: sum
#             Parameter: x[5]
#                 Body:
#                     Var: sum = 0, i;
#                     For (i = 0 , i < 5, 1) Do
#                         sum = sum + i;
#                     EndFor.
#                     Return sum;
#                 EndBody.
#         Function: main
#             Body:
#                 Var: y;
#                 y = sum(x);
#                 printStrLn(string_of_int(y));
#                 Return;
#             EndBody."""
#         expect = str("")
#         self.assertTrue(TestChecker.test(input,expect,494))

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
        self.assertTrue(TestChecker.test(input,expect,467))

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
        self.assertTrue(TestChecker.test(input,expect,468))

    def test_while_stmt_08(self):
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
        self.assertTrue(TestChecker.test(input,expect,469))
