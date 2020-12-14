import unittest
from TestUtils import TestChecker
from StaticError import *
from AST import *

class CheckSuite(unittest.TestCase):
 
    def test_undeclared_var_1(self):
        """Simple program: main"""
        input = """
        Var: b;
        Var: c;

        Function: foo
        Body:
            b = 10;
            b = a + c;
        EndBody.

        Function: main
        Body:
        EndBody.

        """
        expect = str(Undeclared(Variable(),"a"))
        self.assertTrue(TestChecker.test(input,expect,401))

    def test_undeclared_var_2(self):
        """Simple program: main"""
        input = """
        Var: b;
        Var: c = 1.0;
        Var: e;
        Function: foo
        Body:
            b = 10;
            b = e + c;
        EndBody.

        Function: main
        Body:
        EndBody.

        """
        expect = str(TypeMismatchInExpression(BinaryOp('+', Id('e'), Id('c'))))
        self.assertTrue(TestChecker.test(input,expect,402))


    def test_undeclared_var_3(self):
        """Simple program: main"""
        input = """
            Var: b;
            Var: c;
            Var: e;
            Function: foo
            Body:
                b = 10;
                b = e +. c;
            EndBody.
            
            Function: main
            Body:
            EndBody.
            
            """
        expect = str(TypeMismatchInStatement(Assign(Id('b'),BinaryOp('+.', Id('e'), Id('c')))))
        self.assertTrue(TestChecker.test(input, expect, 403))
    
    def test_undeclared_var_4(self):
        """Simple program: main"""
        input = """
            Var: b = 1;
            Var: c;
            Var: e;
            Function: foo
            Body:
                Var: b = True;
                Var: c = 2.0;
                b = e  == c;
            EndBody.
            
            Function: main
            Body:
            EndBody.
            
            """
        expect = str(TypeMismatchInExpression(BinaryOp('==', Id('e'), Id('c'))))
        self.assertTrue(TestChecker.test(input, expect, 404))
    
    def test_undeclared_var_5(self):
        """Simple program: main"""
        input = """
            Var: b = 1.0;
            Var: c;
            Var: e;
            Function: foo
            Body:
                Var: c = 2.0;
                b =  e =/= c;
            EndBody.
            
            Function: main
            Body:
            EndBody.
            
            """
        expect = str(TypeMismatchInStatement(Assign(Id('b'),BinaryOp('=/=',Id('e'),Id('c')))))
        self.assertTrue(TestChecker.test(input, expect, 405))
    
    def test_undeclared_var_6(self):
        """Simple program: main"""
        input = """
            Var: b;
            Var: c;
            Var: e;
            Function: foo
            Body:
                **b =  e =/= c;**
                Var: c = False;
                b = -c;
            EndBody.
            
            Function: main
            Body:
            EndBody.
            
            """
        expect = str(TypeMismatchInExpression(UnaryOp('-',Id('c'))))
        self.assertTrue(TestChecker.test(input, expect, 406))

    def test_undeclared_var_7(self):
        """Simple program: main"""
        input = """
            Var: b = 10;
            Var: c;
            Var: e;
            Function: foo
            Body:
                **b =  e =/= c;**
                Var: c = False;
                b = !c;
            EndBody.
            
            Function: main
            Body:
            EndBody.
            
            """
        expect = str(TypeMismatchInStatement(Assign(Id('b'),UnaryOp('!',Id('c')))))
        self.assertTrue(TestChecker.test(input, expect, 407))
    
    def test_undeclared_var_8(self):
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
            g = 1.0;
            f = b + g;
            EndBody.
            
            """
        expect = str(TypeMismatchInExpression(BinaryOp('+',Id('b'),Id('g'))))
        self.assertTrue(TestChecker.test(input, expect, 408))
    
    def test_undeclared_var_9(self):
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
        self.assertTrue(TestChecker.test(input, expect, 409))
    
    def test_undeclared_var_10(self):
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
        self.assertTrue(TestChecker.test(input, expect, 410))
    
    def test_undeclared_var_11(self):
        """Simple program: main"""
        input = """
            Var: b[1] = 1;
            Function: foo

            Body:
            
            EndBody.
            
            Function: main
            Parameter: x, y ,z
            Body:
            y = x || (x>z); 
            EndBody.
            
            """
        expect = str(TypeMismatchInExpression(BinaryOp('>',Id('x'),Id('z'))))
        self.assertTrue(TestChecker.test(input, expect, 411))
    
    def test_undeclared_var_12(self):
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
        self.assertTrue(TestChecker.test(input, expect, 412))
    
    def test_undeclared_var_13(self):
        """Simple program: main"""
        input = """
            
            Function: foo
            Parameter: a,b,c
            Body:
                a = 2;
                main();
                Return;
            EndBody.
            
            
            Function: foo1
            Parameter: d
            Body:
                d = 10;
                Return;
            EndBody.
                
            
            Function: foo2
            Body:
                Return;
            EndBody.
            
            Function: main
            Parameter: a, b, c
            Body:
                Return "str";
            EndBody.
            
            """
        expect = str(TypeMismatchInStatement(CallStmt(Id('main'),[])))
        self.assertTrue(TestChecker.test(input, expect, 413))
    
    def test_undeclared_var_14(self):
        """Simple program: main"""
        input = """
            
            Function: foo
            Parameter: a,b,c
            Body:
                a = 2;
                
                foo1(1,2,"das");
                main(2,3,1.0);
                Return;
            EndBody.
            
            
            Function: foo1
            Parameter: d, c, e
            Body:
                d = 10;
                Return;
            EndBody.
                
            
            Function: foo2
            Body:
                Return;
            EndBody.
            
            Function: main
            Parameter: a, b, c
            Body:
                a = 10.1;
                Return ;
            EndBody.
            
            """
        expect = str(TypeMismatchInStatement(Assign(Id('a'),FloatLiteral(10.1))))
        self.assertTrue(TestChecker.test(input, expect, 414))
    
    def test_undeclared_var_15(self):
        """Simple program: main"""
        input = """
            
            Function: foo
            Parameter: a,b,c
            Body:
                a = 2;
                
                foo1(1,2,"das");
                main(2,3,1.0);
                Return;
            EndBody.
            
            
            Function: foo1
            Parameter: d, c, e
            Body:
                d = 10;
                e = 0;
                Return;
            EndBody.
                
            
            Function: foo2
            Body:
                Return;
            EndBody.
            
            Function: main
            Parameter: a, b, c
            Body:
                a = 10.1;
                Return ;
            EndBody.
            
            """
        expect = str(TypeMismatchInStatement(Assign(Id('e'),IntLiteral(0))))
        self.assertTrue(TestChecker.test(input, expect, 415))
        
    def test_undeclared_var_16(self):
        """Simple program: main"""
        input = """
            
            Function: foo
            Parameter: a,b,c
            Body:
                a = 2;
                
                foo1(1,2,"das");
                main(2,3,1.0);
                Return;
            EndBody.
            
            
            Function: foo1
            Parameter: d, c, e
            Body:
                d = 10;
                e = "Khanh";
                Return 1;
            EndBody.
                
            
            Function: foo2
            Body:
                Return;
            EndBody.
            
            Function: main
            Parameter: a, b, c
            Body:
                a = 10;
                Return ;
            EndBody.
            
            """
        expect = str(TypeMismatchInStatement(Return(IntLiteral(1))))
        self.assertTrue(TestChecker.test(input, expect, 416))
    
    def test_undeclared_var_17(self):
        """Simple program: main"""
        input = """
            Var: a;
            
            Function: foo
            
            Body:
                Return;
            EndBody.
            
            Function: foo
            Parameter: a,b,c
            Body:
            
            EndBody.
            
            Function: main
            Parameter: a, b, c
            Body:
                Return ;
            EndBody.
            
            """
        expect = str(Redeclared(Function(),'foo'))
        self.assertTrue(TestChecker.test(input, expect, 417))
    
    def test_undeclared_var_18(self):
        """Simple program: main"""
        input = """
            Var: a;
            Var: a,c;
            Function: foo
            Parameter: a,b,c
            Body:
                Return;
            EndBody.
            
            Function: foo
            Body:
            
            EndBody.
            
            Function: main
            Parameter: a, b, c
            Body:
                Return ;
            EndBody.
            
            """
        expect = str(Redeclared(Variable(),'a'))
        self.assertTrue(TestChecker.test(input, expect, 418))
    
    def test_undeclared_var_19(self):
        """Simple program: main"""
        input = """
            Var: a;
            Function: foo
            Parameter: a,b,c
            Body:
                Return;
            EndBody.
            
            Function: main1
            Parameter: a, b, c
            Body:
                Return ;
            EndBody.
            
            """
        expect = str(NoEntryPoint())
        self.assertTrue(TestChecker.test(input, expect, 419))
    
    def test_undeclared_var_20(self):
        """Simple program: main"""
        input = """
            Var: a;
            Function: foo
            Parameter: a,b,c
            Body:
                Return 1;
                main(1,2,3);
            EndBody.
            
            Function: main
            Parameter: a, b, c
            Body:
                Return 1;
            EndBody.
            
            """
        expect = str(TypeMismatchInStatement(Return(IntLiteral(1))))
        self.assertTrue(TestChecker.test(input, expect, 420))
    
    def test_undeclared_var_21(self):
        """Simple program: main"""
        input = """
            Var: a;
            Function: foo
            Parameter: a,b,c
            Body:
                Var: f = 10;
                a = 1;
                b = 2;
                main(1,2,x);
                Return 1;
            EndBody.
            
            Function: foo1
            Body:
                Return 1;
            EndBody.
            
            Function: main
            Parameter: a, b, c
            Body:
                foo1();
                Return ;
            EndBody.
            
            """
        expect = str(Undeclared(Variable(),'x'))
        self.assertTrue(TestChecker.test(input, expect, 421))
    
    def test_undeclared_var_22(self):
        """Simple program: main"""
        input = """
            Var: a;
            Function: foo
            Parameter: a,b,c
            Body:
                Var: f = 10;
                Var: x;
                a = 1;
                b = 2;
                main(1,2,x);
                Return 1;
            EndBody.
            
            Function: foo1
            Body:
                Return 1;
            EndBody.
            
            Function: main
            Parameter: a, b, c
            Body:
                foo1();
                Return ;
            EndBody.
            
            """
        expect = str(TypeCannotBeInferred(CallStmt(Id('main'),[IntLiteral(1),IntLiteral(2),Id('x')])))
        self.assertTrue(TestChecker.test(input, expect, 422))
    
    def test_undeclared_var_23(self):
        """Simple program: main"""
        input = """
            Var: a;
            Function: foo
            Body:
                Var:x ;
                **Var: a = 10;**
                **x = a  + main() + foo1();**
                main(1,2,"string");
                Return 1;
            EndBody.
            
            Function: main
            Parameter: a,b,c
            Body:
                c = 10;
                **foo1();**
                Return ;
            EndBody.
            
            """
        expect = str(TypeMismatchInStatement(Assign(Id('c'),IntLiteral(10))))
        self.assertTrue(TestChecker.test(input, expect, 423))
    
    def test_undeclared_var_24(self):
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
        self.assertTrue(TestChecker.test(input, expect, 424))
    
    def test_undeclared_var_25(self):
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
            EndBody

            Function: main
            Parameter: a,b,c
            Body:
                a = a + 1;
                foo(1,2.0);
                Return 1;
            EndBody.
            
            """
        expect = str(TypeMismatchInStatement(Return(StringLiteral('string'))))
        self.assertTrue(TestChecker.test(input, expect, 425))
    
    def test_undeclared_var_26(self):
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
            EndBody

            Function: main
            Parameter: a,b,c
            Body:
            
                foo(1,2.0);
                Return 1;
            EndBody.
            
            """
        expect = str(TypeMismatchInStatement(Assign(Id('a'),BinaryOp('+',BinaryOp('+',IntLiteral(1),CallExpr(Id('main'),[IntLiteral(1),IntLiteral(2),StringLiteral("string")])),CallExpr(Id('foo1'),[])))))
        self.assertTrue(TestChecker.test(input, expect, 426))
    
    def test_undeclared_var_27(self):
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
            EndBody

            Function: main
            Parameter: a,b,c
            Body:
            
                Return 1;
            EndBody.
            
            """
        expect = str(TypeMismatchInStatement(Assign(Id('a'),CallExpr(Id('foo'),[FloatLiteral(1.0),FloatLiteral(2.0)]))))
        self.assertTrue(TestChecker.test(input, expect, 427))
    
    def test_undeclared_var_28(self):
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
        self.assertTrue(TestChecker.test(input, expect, 428))