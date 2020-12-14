import unittest
from TestUtils import TestChecker
from StaticError import *
from AST import *

class CheckSuite(unittest.TestCase):
    def test_401(self):
        """Created automatically"""
        input = r""" 
        Var: a = 5;
Var: b[2][3] = {{2,3,4},{4,5,6}};
Var: c, d = 6, e, f;
Var: m, n[10];
        """
        expect = str(NoEntryPoint())
        self.assertTrue(TestChecker.test(input,expect,401))
        
    def test_402(self):
        """Created automatically"""
        input = r""" 
        Var: decimal[108], hexadecimal[0X5456A][0x205F], octdecimal[0o413215][0O123];
        Var: array[5][13456];
        """
        expect = str(NoEntryPoint())
        self.assertTrue(TestChecker.test(input,expect,402))
        
    def test_403(self):
        """Created automatically"""
        input = r""" 
        Var: dsa[432][0X364][0o35721], b = 20.e5, c = "mot con vit xoe ra 2 \n cai canh";
        Function: main
        Parameter: a[5][4]
        Body:
            Var: i = 0;
            While (i < 5) Do
                Var: j = 0;
                While ((j % 5) == 2) Do
                    a[i][j] = b +. 1.0;
                    j = j + -i;
                EndWhile.
            EndWhile.
            Return c;
        EndBody.
        """
        expect = str()
        self.assertTrue(TestChecker.test(input,expect,403))
        
    def test_404(self):
        """Created automatically"""
        input = r""" 
        Var: a = True, d = "string\b";
        **this  is comment**
        Function: main
        Parameter: a[123], b , x
        Body:
        Var:y;
            Do
            Var:y; 
            y = y + 1;
                main(a,y,d);
            While (x+y) > 3 EndDo.
        EndBody.
        """
        expect = str(TypeCannotBeInferred(CallStmt(Id("main"),[Id("a"),Id("y"),Id("d")])))
        self.assertTrue(TestChecker.test(input,expect,404))
        
    def test_405(self):
        """Created automatically"""
        input = r""" 
        Var **COMMENT**: ****id = 465632
        **dsfhfsdhjnc^#%#@@~!**;
    Var: sss;Function: main
    Body:
        Var: a = 123;
        If a % 3 == 0 Then
            printStrLn("a % 3 == 0");
        ElseIf a % 3 == 1 Then
            printStrLn("a % 3 == 1");
        Else
            printStrLn("a % 3 == 2");
        EndIf.
    EndBody.
        """
        expect = str()
        self.assertTrue(TestChecker.test(input,expect,405))
        
    def test_406(self):
        """Created automatically"""
        input = r""" 
        Function: main 
        Parameter: global_var
        Body:
            global_var = 25+6-.2.5%3\100 ; 
        EndBody.
        """
        expect = str(TypeMismatchInExpression(BinaryOp("-.",BinaryOp("+",IntLiteral(25),IntLiteral(6)),BinaryOp("\\",BinaryOp("%",FloatLiteral(2.5),IntLiteral(3)),IntLiteral(100)))))
        self.assertTrue(TestChecker.test(input,expect,406))
        
    def test_407(self):
        """Created automatically"""
        input = r"""
        Function: foo
        Parameter: x
        Body:
            Var: a[5]={1,2,3,4};
            Return a;
        EndBody.
        Function: main
        Body:
            Var: a[5]={1,2,3,4};
            Var: b[4];
            Var: c;
            foo(3)[5] = a[1];
            foo(3)[5]=b;
        EndBody.
        """
        expect = str(TypeMismatchInStatement(Assign(ArrayCell(CallExpr(Id("foo"),[IntLiteral(3)]),[IntLiteral(5)]),Id("b"))))
        self.assertTrue(TestChecker.test(input,expect,407))
        
    def test_408(self):
        """Created automatically"""
        input = r""" 
        Function: main
        Parameter: x, y
        Body:
            While (True) Do
                x = main(1, 2);
            EndWhile.
        EndBody.
        """
        expect = str()
        self.assertTrue(TestChecker.test(input,expect,408))
        
    def test_409(self):
        """Created automatically"""
        input = r""" 
        Function: main
        Parameter: x
        Body:
        Var: y = 1;
        main(y);
        x = 1.0;
        EndBody.
        """
        expect = str(TypeMismatchInStatement(Assign(Id("x"),FloatLiteral(1.0))))
        self.assertTrue(TestChecker.test(input,expect,409))
        
    def test_410(self):
        """Created automatically"""
        input = r"""
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
fact (x);
EndBody."""
        expect = str(TypeMismatchInStatement(CallStmt(Id("fact"),[Id("x")])))
        self.assertTrue(TestChecker.test(input,expect,410))
        
    def test_411(self):
        """Created automatically"""
        input = r"""
        Function: main 
        Parameter: a, b,c[123] ,d[123][234][0]  ,e
        Body:
        Var: z[0]={};
            a=1;
        EndBody.
        """
        expect = str()
        self.assertTrue(TestChecker.test(input,expect,411))
        
    def test_412(self):
        """Created automatically"""
        input = r"""
        Var: n;
        Function: fact
        Parameter: themdauchamphay
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
        self.assertTrue(TestChecker.test(input,expect,412))
        
    def test_413(self):
        """Created automatically"""
        input = r"""
                Function: foo
                Parameter: x
                Body:
                EndBody.
                Function: main
                Body:
                    Var: x, y = 0.5;
                    foo(x);
                    y = foo(x);
                EndBody."""
        expect = str(TypeCannotBeInferred(CallStmt(Id("foo"),[Id("x")])))
        self.assertTrue(TestChecker.test(input,expect,413))
        
    def test_414(self):
        """Created automatically"""
        input = r"""Function: main
        Body:
            Var: i = 0;
            Do
                Var: k = 10;
                i = i + 1;
            While i <= 10 
            EndDo.
        EndBody."""
        expect = str()
        self.assertTrue(TestChecker.test(input,expect,414))
        
    def test_415(self):
        """Created automatically"""
        input = r"""
        Function: main
        Parameter: x
        Body:
        Var: y = 1;
        x = 1.0;
        main(y);
        EndBody."""
        expect = str(TypeMismatchInStatement(CallStmt(Id("main"),[Id("y")])))
        self.assertTrue(TestChecker.test(input,expect,415))
        
    def test_416(self):
        """Created automatically"""
        input = r"""
        Function: main
        Body:
            Var: foo = 0;
            foo = foo + foo();
        EndBody.
        Function: foo
        Body:
            Return True;
        EndBody."""
        expect = str(Undeclared(Function(),"foo"))
        self.assertTrue(TestChecker.test(input,expect,416))
        
    def test_417(self):
        """Created automatically"""
        input = r"""
        Function: main 
        Parameter: x, a
        Body:
            While x>1 Do
                Var: a = 10;
            EndWhile.
        EndBody.
        """
        expect = str()
        self.assertTrue(TestChecker.test(input,expect,417))
        
    def test_418(self):
        """Created automatically"""
        input = r"""
        Function: main
        Parameter: x, y
        Body:
            Var: z;
            While (True) Do
                z = main(1, main(x, True));
            EndWhile.
            Return y && z;
        EndBody."""
        expect = str(TypeCannotBeInferred(Assign(Id("z"),CallExpr(Id("main"),[IntLiteral(1),CallExpr(Id("main"),[Id("x"),BooleanLiteral(True)])]))))
        self.assertTrue(TestChecker.test(input,expect,418))
        
    def test_419(self):
        """Created automatically"""
        input = r"""Var **test comment**: **bien = "STRING"**
        ****fu[3]={0X743A5,0o26523,321 **cmt**},i****;****
        Function: main
            Body:
            Var:x,y,j;
                For (i=0, True, 1) Do
                    x = y + 1;
                EndFor.
                
                For (j=1, True, main()) Do
                    y = x + 1;
                EndFor.
            EndBody.
            """
        expect = str()
        self.assertTrue(TestChecker.test(input,expect,419))
        
    def test_420(self):
        """Created automatically"""
        input = r"""Function: main 
        Parameter: varrr
        Body:
            Var: x =1;
            Do
                Var: x =1.5;
                x= x+.1.5;
            While x>1 
            EndDo.
        EndBody."""
        expect = str()
        self.assertTrue(TestChecker.test(input,expect,420))
        
    def test_421(self):
        """Created automatically"""
        input = r"""
        Var: a[1] = {0};

Function: foo
    Parameter: x
    Body:
        Return a;
    EndBody.

Function: main
    Body:
        foo(0)[0] = foo(0.0)[0];
    EndBody."""
        expect = str(TypeMismatchInExpression(CallExpr(Id("foo"),[FloatLiteral(0.0)])))
        self.assertTrue(TestChecker.test(input,expect,421))
        
    def test_422(self):
        """Created automatically"""
        input = r"""Var: a =True;Function:main Parameter:x,b Body:If!a Thenb=2; ElseWhile(x>0)DoBreak;EndWhile.EndIf.EndBody."""
        expect = str()
        self.assertTrue(TestChecker.test(input,expect,422))
        
    def test_423(self):
        """Created automatically"""
        input = r"""Function: main 
        Parameter: n
        Body:
            If n <=. 1.2E-4 Then
            n=n*.3.3;
            ElseIf n>.100.2 Then
            n=n\.5;
            EndIf.
        EndBody.
        """
        expect = str(TypeMismatchInExpression(BinaryOp("\.",Id("n"),IntLiteral(5))))
        self.assertTrue(TestChecker.test(input,expect,423))
        
    def test_424(self):
        """Created automatically"""
        input = r"""Function: main 
        Body:
        Var: k,i;
            If ((k==1)&&(i!=0))||(k==5.6)||!j Then
                f=f%3;
            EndIf.
        EndBody."""
        expect = str(TypeMismatchInExpression(BinaryOp("==",Id("k"),FloatLiteral(5.6))))
        self.assertTrue(TestChecker.test(input,expect,424))
        
    def test_425(self):
        """Created automatically"""
        input = r"""Function: main 
        Parameter: n
        Body:
            Var: a[3] = {1,2,3}, b[2][3], c[2][3] = {{1,3},{3,5,7}};
            a[3+foo(3)] = a[b[2][3]] + 4;
        EndBody."""
        expect = str(Undeclared(Function(),"foo"))
        self.assertTrue(TestChecker.test(input,expect,425))
        
    def test_426(self):
        """Created automatically"""
        input = r"""
        Var: a,b,c,d;
        Function: main 
        Parameter: n
        Body:
        Var: x;
            x = !(!(!a && b) || (c >. 3.e+3) &&!(d < 2));
        EndBody."""
        expect = str()
        self.assertTrue(TestChecker.test(input,expect,426))
        
    def test_427(self):
        """Created automatically"""
        input = r"""
        Var: x, y[1][3]={{{12,1}, {12., 12e3}},{23}, {13,32}};
        Function: main 
        Parameter: xonxon
        Body:
            Var: var;
            Var: ilv, nvh;
            var = (x==123)!= xonxon ;
            x = var && (ilv <. nvh);
        EndBody."""
        expect = str(TypeMismatchInExpression(BinaryOp("!=",BinaryOp("==",Id("x"),IntLiteral(123)),Id("xonxon"))))
        self.assertTrue(TestChecker.test(input,expect,427))
        
    def test_428(self):
        """Created automatically"""
        input = r"""Var: a;
        Function: main 
        Parameter: n, arr[3][4][5]
        Body:
            a = 3*.4.5\0e-2+arr[3-main("call")];
        EndBody."""
        expect = str(TypeMismatchInExpression(BinaryOp("*.",IntLiteral(3),FloatLiteral(4.5))))
        self.assertTrue(TestChecker.test(input,expect,428))
        
    def test_429(self):
        """Created automatically"""
        input = r"""
        Var: a[5];
        Function: main 
        Parameter: x
        Body:
            x = -(-15.e-1+(-.45.1*.2.3)*(35+108+a[4]));
        EndBody."""
        expect = str(TypeMismatchInExpression(UnaryOp("-",FloatLiteral(1.5))))
        self.assertTrue(TestChecker.test(input,expect,429))
        
    def test_430(self):
        """Created automatically"""
        input = r"""Var:c[4][5],b[108];
        Function: main 
        Parameter: i , j, arr[1001]
        Body:
        Var:a[2005];
            a[i] = arr[c[2+j][b[i]*3]] + 4;
            i = i + 1;
        EndBody."""
        expect = str()
        self.assertTrue(TestChecker.test(input,expect,430))
        
    def test_431(self):
        """Created automatically"""
        input = r"""
        Var:var;
        Function: main 
        Parameter: a
        Body:
        Var: variable;
            While (True) Do
            Var: logic;
                logic=a&&var||!variable;
            EndWhile.
        EndBody."""
        expect = str()
        self.assertTrue(TestChecker.test(input,expect,431))
        
    def test_432(self):
        """Created automatically"""
        input = r"""
        Var: a,c,d;
        Function: main
        Parameter: b
        Body:
        Var: d;
            a = -1082000;
            b = -0X123BCD;
            c = -0o21345;
            d = -a;
            c = -call(a);
        EndBody.
        Function: call
                Parameter: s
                Body:
                    Return 0;
                EndBody.
                """
        expect = str()
        self.assertTrue(TestChecker.test(input,expect,432))
        
    def test_433(self):
        """Created automatically"""
        input = r"""
        Var: a[143];
        Function: main
        Parameter: n,b[15]
        Body:
            a[a[3 + foo(2,2.6)]] = a[b[b||True]]+b[1+0x369]*3 + 4;
        EndBody.
        Function: foo
        Parameter: a,b
        Body:
            Return 2;
        EndBody."""
        expect = str(TypeMismatchInExpression(BinaryOp("||",Id("b"),BooleanLiteral(True))))
        self.assertTrue(TestChecker.test(input,expect,433))
        
    def test_434(self):
        """Created automatically"""
        input = r"""Function: main
        Parameter: arr[2222]
        Body:
        Var: x,a=0X24211ABC;
            x=arr[a+6];
        EndBody."""
        expect = str(TypeCannotBeInferred(Assign(Id("x"),ArrayCell(Id("arr"),[BinaryOp("+",Id("a"),IntLiteral(6))]))))
        self.assertTrue(TestChecker.test(input,expect,434))
        
    def test_435(self):
        """Created automatically"""
        input = r"""Function: main 
        Parameter: a
        Body:
        Var: x; 
            x = (a >=. 2.3e-13 || (x =/= 2e-35));
        EndBody."""
        expect = str(TypeMismatchInExpression(BinaryOp("||",FloatLiteral(2.3e-13),BinaryOp("=/=",Id("x"),FloatLiteral(2e-35)))))
        self.assertTrue(TestChecker.test(input,expect,435))
        
    def test_436(self):
        """Created automatically"""
        input = r"""
        Function: main
        Body:
            Var: x=1;
            If x > 10 Then
                x=25+6-.2.5%3\100*x;
            Else
                x=x+2;
            EndIf.
        EndBody."""
        expect = str(TypeMismatchInExpression(BinaryOp("-.",BinaryOp("+",IntLiteral(25),IntLiteral(6)),BinaryOp("*",BinaryOp("\\",BinaryOp("%",FloatLiteral(2.5),IntLiteral(3)),IntLiteral(100)),Id("x")))))
        self.assertTrue(TestChecker.test(input,expect,436))
        
    def test_437(self):
        """Created automatically"""
        input = r"""Var: x[5] = {1,2,3,4,5};
        Function: sum
            Parameter: x[5]
                Body:
                    Var: sum = 0, i;
                    For (i = 0 , i < 5, 1) Do
                        sum = sum + i;
                    EndFor.
                    Return sum;
                EndBody.
        Function: main
            Body:
                Var: y;
                y = sum(x);
                printStrLn(string_of_int(y));
                Return;
            EndBody."""
        expect = str()
        self.assertTrue(TestChecker.test(input,expect,437))
        
    def test_438(self):
        """Created automatically"""
        input = r"""Function: main 
        Parameter: n,a[3], b[2][3], c[1]
        Body:a = {1,2,3}; b[2][3] = 5;
        c[2] = {{1,3},{1,5,7}};
        EndBody."""
        expect = str(TypeMismatchInStatement(Assign(ArrayCell(Id("c"),[IntLiteral(2)]),ArrayLiteral([ArrayLiteral([IntLiteral(1),IntLiteral(3)]),ArrayLiteral([IntLiteral(1),IntLiteral(5),IntLiteral(7)])]))))
        self.assertTrue(TestChecker.test(input,expect,438))
        
    def test_439(self):
        """Created automatically"""
        input = r"""Function: main 
        Body:
            Var: a;
                If bool_of_string("True") Then
                Var: b;
                    a = int_of_string (b);
                    b = float_of_int (a) +. 2.0;
                EndIf.
        EndBody."""
        expect = str(Undeclared(Function(),"float_of_int"))
        self.assertTrue(TestChecker.test(input,expect,439))
        
    def test_440(self):
        """Created automatically"""
        input = r"""Function: main
        Parameter: n
        Body:
        Var: a, b;
            If bool_of_string("True") Then
                a = int_of_string (read ());
            ElseIf n =/= 1.08 Then
                b = float_of_int (a) +. 2.0;
            ElseIf False Then
                Return n;
            EndIf.
        EndBody."""
        expect = str(Undeclared(Function(),"float_of_int"))
        self.assertTrue(TestChecker.test(input,expect,440))
        
    def test_441(self):
        """Created automatically"""
        input = r"""
        Var: x, a,b ,c;
        Function: main 
        Body:
        Var:a,b,c;
            If (x == (b!=c && (a > b + c))) Then Return;
            ElseIf (x=="Chung Xon@@") Then Break;
            Else 
            x="successful";
            EndIf.
        EndBody."""
        expect = str(TypeMismatchInExpression(BinaryOp("+",Id("b"),Id("c"))))
        self.assertTrue(TestChecker.test(input,expect,441))
        
    def test_442(self):
        """Created automatically"""
        input = r"""
        Var: i;
        Function: main
        Body:
        Var: n;
            If i <. 4.5 Then
                printStrLn(string_of_float(i));
            ElseIf n > 10 Then 
                Break;
            Else
                i=int_of_float(i)-1;
            EndIf.
            EndBody."""
        expect = str(TypeMismatchInStatement(Assign(Id("i"),BinaryOp("-",CallExpr(Id("int_of_float"),[Id("i")]),IntLiteral(1)))))
        self.assertTrue(TestChecker.test(input,expect,442))
        
    def test_443(self):
        """Created automatically"""
        input = r"""Function: main
        Parameter: a, b
        Body:
        Var: id[4312][867][9856][867], literal = 120000e-1,  array[2][3] = {{867,345,987},{76,12,744}};
            If n > 10 Then
                If n <. 20.5 Then Return x;
                EndIf.
                printStrLn(arg);
            Else fact(x);
            EndIf.
        EndBody."""
        expect = str(Undeclared(Identifier(),"n"))
        self.assertTrue(TestChecker.test(input,expect,443))
        
    def test_444(self):
        """Created automatically"""
        input = r"""
        Function: main
        Body:
        Var: i = 0, a;
            For (i = 0, i < 10, 2) Do
                a= int_of_float(float_of_string(read()));
                Return a;
            EndFor.
        EndBody."""
        expect = str()
        self.assertTrue(TestChecker.test(input,expect,444))
        
    def test_445(self):
        """Created automatically"""
        input = r"""
        Function: main 
        Parameter: n[5],i
        Body:
            For (i = 0, i < 10, 1) Do
                n[i]=n[i]+i;
            EndFor.
        EndBody."""
        expect = str()
        self.assertTrue(TestChecker.test(input,expect,445))
        
    def test_446(self):
        """Created automatically"""
        input = r"""
        Var: i=0, k=100;
        Function: main
        Body:
            For (i=12, i < k, i*i) Do
            goo();
            EndFor.
        EndBody."""
        expect = str(Undeclared(Function(),"goo"))
        self.assertTrue(TestChecker.test(input,expect,446))
        
    def test_447(self):
        """Created automatically"""
        input = r"""
        Function: main
        Body:
        Var: i , x;
            For (i = 1, i <= x*x,i*i+.1.5)
            Do x=x+1;
            EndFor.
        EndBody."""
        expect = str(TypeMismatchInExpression(BinaryOp("+.",BinaryOp("*",Id("i"),Id("i")),FloatLiteral(1.5))))
        self.assertTrue(TestChecker.test(input,expect,447))
        
    def test_448(self):
        """Created automatically"""
        input = r"""
        Function: main
        Parameter: row,col,sum,arr[5][9]
        Body:
            Var: sum=0;
            For( i=0,i<=row,1) Do
                For(j=0,j<col,2) Do
                    sum=sum+arr[i][j];
                EndFor.
            EndFor.
        EndBody."""
        expect = str(Redeclared(Variable(),"sum"))
        self.assertTrue(TestChecker.test(input,expect,448))
        
    def test_449(self):
        """Created automatically"""
        input = r"""Function: main
        Body:
            Var: i = 0,k=10;
            While i !=k Do
            Var:a[5],b, c = "Hello";
                a[i] = b + i + int_of_string();
                i = i + 1;
            EndWhile.
        EndBody."""
        expect = str(TypeMismatchInExpression(CallExpr(Id("int_of_string"),[])))
        self.assertTrue(TestChecker.test(input,expect,449))
        
    def test_450(self):
        """Created automatically"""
        input = r"""Function: main 
        Body:
            Var: x=20;
            While True Do
                If x==0 Then Break;
                ElseIf x%2==0 Then
                    x=x\2;
                Else printStrLn("Error");
                EndIf.
            EndWhile.
        EndBody."""
        expect = str()
        self.assertTrue(TestChecker.test(input,expect,450))
        
    def test_451(self):
        """Created automatically"""
        input = r"""Function: main
        Body:
        Var:i = 10;
            While i < 5 Do Return; EndWhile.
        EndBody."""
        expect = str()
        self.assertTrue(TestChecker.test(input,expect,451))
        
    def test_452(self):
        """Created automatically"""
        input = r"""Function: main 
        Parameter: x
        Body:
            While (True) Do
                While (x>=0) Do
                    x = x+-1;
                EndWhile.
                If ((x<0)) Then Break; EndIf.
            EndWhile.
        EndBody."""
        expect = str()
        self.assertTrue(TestChecker.test(input,expect,452))
        
    def test_453(self):
        """Created automatically"""
        input = r"""Function: main 
        Parameter: n
        Body:
            While True Do
                Whilen>=1 Do
                    Whilen<.69.96 Do
                        While n%3==1 Do
                            n = n \ 5;
                        EndWhile
                    .EndWhile.
                EndWhile.
            EndWhile.
        EndBody."""
        expect = str(TypeMismatchInExpression(BinaryOp("<.",Id("n"),FloatLiteral(69.96))))
        self.assertTrue(TestChecker.test(input,expect,453))
        
    def test_454(self):
        """Created automatically"""
        input = r"""
        Function: main
        Body:
            While True Do printStrLn("Hello World"); EndWhile.
        EndBody."""
        expect = str()
        self.assertTrue(TestChecker.test(input,expect,454))
        
    def test_455(self):
        """Created automatically"""
        input = r"""Function: main
        Parameter: a
        Body:
            Do
                While a<100 Do
                    a=a-30;
                EndWhile.
            While (a>.1.5)
            EndDo.
        EndBody."""
        expect = str(TypeMismatchInExpression(BinaryOp(">.",Id("a"),FloatLiteral(1.5))))
        self.assertTrue(TestChecker.test(input,expect,455))
        
    def test_456(self):
        """Created automatically"""
        input = r"""Function: main
        Parameter: x,a,b
        Body:
            Do x = a + b;
            While(x<1000.e5)
            EndDo.
        EndBody."""
        expect = str(TypeMismatchInExpression(BinaryOp("<",Id("x"),FloatLiteral(100000000.0))))
        self.assertTrue(TestChecker.test(input,expect,456))
        
    def test_457(self):
        """Created automatically"""
        input = r"""Function: main 
        Parameter: a
        Body:
            Do  
                Return a;
            While a =/= 2.2 EndDo.
        EndBody."""
        expect = str(TypeCannotBeInferred(Return(Id("a"))))
        self.assertTrue(TestChecker.test(input,expect,457))
        
    def test_458(self):
        """Created automatically"""
        input = r"""Function: main 
        Parameter: x
        Body:
            While x >= 1 Do
            Var: y;
                If y<100 Then Break;
                EndIf.
            EndWhile.
            
        EndBody."""
        expect = str()
        self.assertTrue(TestChecker.test(input,expect,458))
        
    def test_459(self):
        """Created automatically"""
        input = r"""Function: main
        Body:
        Var:i=0;
            For (i=0, i!=9, (i*.2.0)) Do
                If i>=10 Then Break;
                EndIf.
            EndFor.
        EndBody."""
        expect = str(TypeMismatchInExpression(BinaryOp("*.",Id("i"),FloatLiteral(2.0))))
        self.assertTrue(TestChecker.test(input,expect,459))
        
    def test_460(self):
        """Created automatically"""
        input = r"""
        Function: foo
        Body:
            Var: c[3];
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
        expect = str(TypeCannotBeInferred(Return(Id("c"))))
        self.assertTrue(TestChecker.test(input,expect,460))
        
    def test_461(self):
        """Created automatically"""
        input = r"""
        Function: call
        Parameter: a, b, c, d, e,f
        Body:
            Return f;
        EndBody.
        Function: main
        Body:
        Var: a, var, arr[5]={1};
            call(a,876,var*.65e-1,arr[3],True,"chuoi~~\n");
        EndBody."""
        expect = str(TypeCannotBeInferred(Return(Id("f"))))
        self.assertTrue(TestChecker.test(input,expect,461))
        
    def test_462(self):
        """Created automatically"""
        input = r"""Function: main 
        Parameter: x,y
        Body:
            foo(2 + x, 4. \. y);
            goo();
        EndBody.
        Function: foo
        Body:
            Var: a, c;
            Return a + b;
        EndBody."""
        expect = str(TypeMismatchInStatement(CallStmt(Id("foo"),[BinaryOp("+",IntLiteral(2),Id("x")),BinaryOp("\.",FloatLiteral(4.0),Id("y"))])))
        self.assertTrue(TestChecker.test(input,expect,462))
        
    def test_463(self):
        """Created automatically"""
        input = r"""
        Function: call
        Parameter: a, b, c, d, e,f
        Body:
            Return f;
        EndBody.
        Function: main
        Body:
        Var: a, var, arr[5]={1};
            a = call(a,876,var*.65e-1,arr[3],True,"chuoi~~\n") +1;
        EndBody."""
        expect = str(TypeCannotBeInferred(Return(Id("f"))))
        self.assertTrue(TestChecker.test(input,expect,463))
        
    def test_464(self):
        """Created automatically"""
        input = r"""Var: callnotinfunction;
        Function: main
        Body:
            goo(x,y*2,z+3.00000003);
            EndBody."""
        expect = str(Undeclared(Function(),"goo"))
        self.assertTrue(TestChecker.test(input,expect,464))
        
    def test_465(self):
        """Created automatically"""
        input = r"""Function: main
        Body:
            print(string_of_bool(!bool_of_string("False")&&!True));
        EndBody."""
        expect = str()
        self.assertTrue(TestChecker.test(input,expect,465))
        
    def test_466(self):
        """Created automatically"""
        input = r"""Function: main 
        Parameter: n
        Body:
            Var: t=False;
            If n<100 Then t=True;
            EndIf.
            Return t;
        EndBody."""
        expect = str()
        self.assertTrue(TestChecker.test(input,expect,466))
        
    def test_467(self):
        """Created automatically"""
        input = r"""Function: main
    Body:
        Var: x;
        Do
            x = 1;
        While x
        EndDo.
    EndBody."""
        expect = str(TypeMismatchInStatement(Dowhile(([],[Assign(Id("x"),IntLiteral(1))]),Id("x"))))
        self.assertTrue(TestChecker.test(input,expect,467))
        
    def test_468(self):
        """Created automatically"""
        input = r"""
        Var: x;
        Function: foo
            Parameter: x[3]
            Body:
                Return;
            EndBody.
        Function: main
            Body:
                Return foo({1.1,2.2,3.3});
            EndBody."""
        expect = str(TypeMismatchInStatement(Return(CallExpr(Id("foo"),[ArrayLiteral([FloatLiteral(1.1),FloatLiteral(2.2),FloatLiteral(3.3)])]))))
        self.assertTrue(TestChecker.test(input,expect,468))
        
    def test_469(self):
        """Created automatically"""
        input = r"""
            Function: main
            Body:
            If "str" == "Chung Xon" Then
                Return True;
            Else
                Return False;
                EndIf.
            EndBody."""
        expect = str(TypeMismatchInExpression(BinaryOp("==",StringLiteral("str"),StringLiteral("Chung Xon"))))
        self.assertTrue(TestChecker.test(input,expect,469))
        
    def test_470(self):
        """Created automatically"""
        input = r"""
        Var: a;
        Function: main 
        Body:
        Var: a;
        Return int_of_float(a+.2.5)+foo(int_of_float(a));
        EndBody.
        Function: foo
        Parameter: x
        Body:
        Return x == a;
        EndBody."""
        expect = str(TypeMismatchInStatement(Return(BinaryOp("==",Id("x"),Id("a")))))
        self.assertTrue(TestChecker.test(input,expect,470))
        
    def test_471(self):
        """Created automatically"""
        input = r"""Function: main
        Parameter: x[123]
        Body:
            Var: i = 0;
            x={996.24,712.464,216.454};
            printStrLn(string_of_float(x[2]));
            printStrLn(string_of_int(x[2]));
        EndBody."""
        expect = str(TypeMismatchInStatement(Assign(Id("x"),ArrayLiteral([FloatLiteral(996.24),FloatLiteral(712.464),FloatLiteral(216.454)]))))
        self.assertTrue(TestChecker.test(input,expect,471))
        
    def test_472(self):
        """Created automatically"""
        input = r"""Function: main 
                Parameter: x[2][3]
        Body:
            Var: i = 0;
            x[2][3]={{867,345,987},{76,12,744}};
            printStrLn(string_of_int(x[2]));
        EndBody."""
        expect = str(TypeMismatchInStatement(Assign(ArrayCell(Id("x"),[IntLiteral(2),IntLiteral(3)]),ArrayLiteral([ArrayLiteral([IntLiteral(867),IntLiteral(345),IntLiteral(987)]),ArrayLiteral([IntLiteral(76),IntLiteral(12),IntLiteral(744)])]))))
        self.assertTrue(TestChecker.test(input,expect,472))
        
    def test_473(self):
        """Created automatically"""
        input = r"""
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
        self.assertTrue(TestChecker.test(input,expect,473))
        
    def test_474(self):
        """Created automatically"""
        input = r"""Function: main
        Body:
            Var  : x[123]={   20, 2   ,108  };
        EndBody."""
        expect = str()
        self.assertTrue(TestChecker.test(input,expect,474))
        
    def test_475(self):
        """Created automatically"""
        input = r"""
        Function: main
        Body:
            foo()[0] = 1;
        EndBody.

        Function: foo
        Body:
        EndBody."""
        expect = str(TypeCannotBeInferred(Assign(ArrayCell(CallExpr(Id("foo"),[]),[IntLiteral(0)]),IntLiteral(1))))
        self.assertTrue(TestChecker.test(input,expect,475))
        
    def test_476(self):
        """Created automatically"""
        input = r"""Function: main
        Body:
            Var: a[12] = { 5 };
            Var: x[45]={{{{{5}}}}};

        EndBody."""
        expect = str()
        self.assertTrue(TestChecker.test(input,expect,476))
        
    def test_477(self):
        """Created automatically"""
        input = r"""
        Var: arr[5];
        Function: func1
        Parameter: x
        Body:
        Return x *x%2;
        EndBody.
        Function: main
        Parameter: a
        Body:
            a =float_of_int(-(-(func1(4)+23) * -func2(a)+arr[3]))\. 0.5;
        EndBody.
        Function: func2
        Parameter: y
        Body:
        Var: z;
        Var: i = 0;
        While (i < 5) Do
            z = z +. y;
            i = i + 1;
        EndWhile.
        Return z;
        EndBody."""
        expect = str(Undeclared(Function(),"float_of_int"))
        self.assertTrue(TestChecker.test(input,expect,477))
        
    def test_478(self):
        """Created automatically"""
        input = r"""
        Function: func2 
        Parameter: n
        Body: 
            If n == 0 Then
                Return 1;
            Else
                Return n * func2 (n - 1);
            EndIf.
        EndBody.
        Function: goo 
        Parameter: n
        Body: ** Xin chao**
        Var: string = "Xin chao";
        Return 108;
        EndBody.
        Function: main
        Body:
        Var: a;
            a =func1(func2(3))+23 - foo(goo(func1(a)));
        EndBody.
        Function: func1
        Parameter: x
        Body:
        Var: a, b, c;
            If(x == ((False||True) && (a > b + c))) Then
                a = b - c;
            Else
                a = b + c;
                x = True;
            EndIf.
        EndBody.
        Function: foo 
        Parameter: n
        Body: 
            While(1) Do
                n = True;
            EndWhile.
        EndBody.
        """
        expect = str(TypeMismatchInExpression(BinaryOp("==",Id("x"),BinaryOp("&&",BinaryOp("||",BooleanLiteral(False),BooleanLiteral(True)),BinaryOp(">",Id("a"),BinaryOp("+",Id("b"),Id("c")))))))
        self.assertTrue(TestChecker.test(input,expect,478))
        
    def test_479(self):
        """Created automatically"""
        input = r"""Function: a Parameter: a Body:Var: a=False;EndBody. Function: b Body:EndBody.
Function: main**Here some too**Parameter: d Body:EndBody."""
        expect = str(Redeclared(Variable(),"a"))
        self.assertTrue(TestChecker.test(input,expect,479))
        
    def test_480(self):
        """Created automatically"""
        input = r"""Function: main 
        Parameter: n,a,b
        Body:
            Var: i = 0,c;
            While i!=423 Do
                i = i + 3; **cmt**
                If i==212 Then Break;
                a = (!(b && c)||!(a&&b)&&(i+1)==234); 
                EndIf.
            EndWhile.
        EndBody.
        """
        expect = str(TypeMismatchInExpression(BinaryOp("&&",BinaryOp("||",UnaryOp("!",BinaryOp("&&",Id("b"),Id("c"))),UnaryOp("!",BinaryOp("&&",Id("a"),Id("b")))),BinaryOp("+",Id("i"),IntLiteral(1)))))
        self.assertTrue(TestChecker.test(input,expect,480))
        
    def test_481(self):
        """Created automatically"""
        input = r"""Function: main
        Body:
            Do
                While(1) Do
                foo (2 + x, 4. \. y);
                goo ();
            EndWhile.
            While(1)
            EndDo.
        EndBody."""
        expect = str(TypeMismatchInStatement(While(IntLiteral(1),([],[CallStmt(Id("foo"),[BinaryOp("+",IntLiteral(2),Id("x")),BinaryOp("\.",FloatLiteral(4.0),Id("y"))]),CallStmt(Id("goo"),[])]))))
        self.assertTrue(TestChecker.test(input,expect,481))
        
    def test_482(self):
        """Created automatically"""
        input = r"""Function: main
        Parameter: a[5], b
        Body:
        Var: x[2][3] = {{1,2,3},{2,3,3}};
        Var: i = 0;
        While (i < 5) Do
        If i == 3 ThenReturn 1;EndIf.
        i = i + 1;
        EndWhile.
        Return x[1][1];
        EndBody."""
        expect = str()
        self.assertTrue(TestChecker.test(input,expect,482))
        
    def test_483(self):
        """Created automatically"""
        input = r"""Function: main
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
        self.assertTrue(TestChecker.test(input,expect,483))
        
    def test_484(self):
        """Created automatically"""
        input = r"""Function: main
        Parameter: n
        Body:
            Var: t1 = 0, t2 = 1, nextTerm = 0, i;
            print("Enter the number of terms: ");
            n = int_of_string(read());
            print("Fibonacci Series: ");
            For (i = 1, i <= n, 1) Do
                If(i == 1) Then
                print(string_of_int(t1));
                Continue;
                EndIf.
            If(i == 2) Then
                print("t2");
        Continue;
        EndIf.
        nextTerm = t1 + t2;
        t1 = t2;
        t2 = nextTerm;
        
        print(string_of_int(nextTerm));
    EndFor.
    Return 0;
    EndBody."""
        expect = str()
        self.assertTrue(TestChecker.test(input,expect,484))
        
    def test_485(self):
        """Created automatically"""
        input = r"""Function: main
        Parameter: octalNumber
        Body:
        Var: decimalNumber = 0, i = 0, rem;
        While (octalNumber != 0) Do
            rem = octalNumber % 10;
            octalNumber =octalNumber \ 10;
            decimalNumber =decimalNumber  + rem * pow(8,i);
            i=i+1;
        EndWhile.
    Return decimalNumber;
    EndBody.
    Function: pow
    Parameter: x,y
    Body:
    If x == 0 Then
    Return 1;
    EndIf.
    Return x * pow(x-1,y);
    EndBody."""
        expect = str()
        self.assertTrue(TestChecker.test(input,expect,485))
        
    def test_486(self):
        """Created automatically"""
        input = r""" 
        Function: func2 
        Parameter: n
        Body: 
            If n == 0 Then
                Return 1;
            Else
                Return n * func2 (n - 1);
            EndIf.
        EndBody.
        Function: main
        Body:
        Var: a;
            a =func1(func2(3))+23 - foo(goo(func1(a)));
        EndBody.
        Function: goo 
        Parameter: n
        Body: ** Xin chao**
        Var: string = "Xin chao";
        Return 108;
        EndBody.
        Function: func1
        Parameter: x
        Body:
        Var: a, b, c;
            If(x == ((False||True) && (a > b + c))) Then
                a = b - c;
            Else
                a = b + c;
                x = True;
            EndIf.
        EndBody.
        Function: foo 
        Parameter: n
        Body: 
            While(1) Do
                n = True;
            EndWhile.
        EndBody.
                """
        expect = str(TypeCannotBeInferred(Assign(Id("a"),BinaryOp("-",BinaryOp("+",CallExpr(Id("func1"),[CallExpr(Id("func2"),[IntLiteral(3)])]),IntLiteral(23)),CallExpr(Id("foo"),[CallExpr(Id("goo"),[CallExpr(Id("func1"),[Id("a")])])])))))
        self.assertTrue(TestChecker.test(input,expect,486))
        
    def test_487(self):
        """Created automatically"""
        input = r"""Function: main 
        Body:
        Var: n;
            If n == 0 Then
                Break;
            EndIf.
        EndBody."""
        expect = str()
        self.assertTrue(TestChecker.test(input,expect,487))
        
    def test_488(self):
        """Created automatically"""
        input = r"""Function: main 
        Body:
            If n == 0 Then
                x = 3;
            ElseIf x != 2 Then
                check = False;
            EndIf.
        EndBody."""
        expect = str(Undeclared(Identifier(),"n"))
        self.assertTrue(TestChecker.test(input,expect,488))
        
    def test_489(self):
        """Created automatically"""
        input = r"""Var: a[2] = {True,{2,3}}, str = "string",c,d;
        Function: func
        Body:
        Var: j,k=2,b=1.1234e-3,i;
            If (((a + 5) * (j-6)) !=0) || ((k*7) >=100) Then
               
                a[i] = int_of_float(b +. 1.0);
                b = float_of_int(i - int_of_float(b) * a) -. b \. c -. -.d;
            EndIf.
            Return a+func(123);
        EndBody.
        Function: main
        Body:
            func();
            Return 0;
        EndBody."""
        expect = str(TypeMismatchInExpression(BinaryOp("+",Id("a"),IntLiteral(5))))
        self.assertTrue(TestChecker.test(input,expect,489))
        
    def test_490(self):
        """Created automatically"""
        input = r"""** this is a comment **
        Var: a[2] = {True,{2,3}}, str = "string";
        Function: func
        Body:
            If (a + 5) && (j-6) || (k*7) Then
                ** this is another comment **
                a[i] = b +. 1.0;
                b = i - b * a -. b \ c - -.d;
            EndIf.
            Return a+func();
        EndBody.
        Function: main
        Body:
            func();
            Return 0;
        EndBody."""
        expect = str(TypeMismatchInExpression(BinaryOp("+",Id("a"),IntLiteral(5))))
        self.assertTrue(TestChecker.test(input,expect,490))
        
    def test_491(self):
        """Created automatically"""
        input = r"""Var: a = 5;

        Function: main
        Parameter: a
        Body:
        Var:b[2];
            If bool_of_string ("True") Then
                a = int_of_string (read ());
                b = float_of_int (a) +. 2.0;
            ElseIf a == 5 Then
                a = a + main(123);
            ElseIf a == 6 Then
                a = a * 2;
                Return string_of_int(a);
                Break;
            Else Continue;
            EndIf.
        EndBody."""
        expect = str(Undeclared(Function(),"float_of_int"))
        self.assertTrue(TestChecker.test(input,expect,491))
        
    def test_492(self):
        """Created automatically"""
        input = r"""Function: main
                    Parameter: x
                    Body:
                    Var: i, result;
                        For (i = 1, i <= x*x*x,i + x ) Do
                            result = i * i + i \ --1 % i--i;
                        EndFor.
                        Return result;
                    EndBody."""
        expect = str()
        self.assertTrue(TestChecker.test(input,expect,492))
        
    def test_493(self):
        """Created automatically"""
        input = r"""
            Function: sqrt
            Parameter: x
            Body:
                Var: i;
            While (i*i) < x Do
                    i = i - -1;
                EndWhile.
                Return i-1;
            EndBody.
            Function: main
            Parameter: n,x
            Body:
                Var: i;
                For (i = 0, i < sqrt(n), 2) Do
                    x = i + n;
                EndFor.
            EndBody."""
        expect = str()
        self.assertTrue(TestChecker.test(input,expect,493))
        
    def test_494(self):
        """Created automatically"""
        input = r"""Function: main
        Body:
            m = test2(a,b) + main (x);
        EndBody.
        Function: test2
        Body:
            Do
                If(z == 1) Then
                    x = !a;
                EndIf.
            While x
            EndDo.
        EndBody."""
        expect = str(Undeclared(Identifier(),"m"))
        self.assertTrue(TestChecker.test(input,expect,494))
        
    def test_495(self):
        """Created automatically"""
        input = r"""Function: main 
        Body:
        Var:x;
            While x>1 Do
            Var: i,a = 4;
                For (i = 100,True, i-1) Do
                    If -a<-3 Then
                        Break;
                    EndIf.
                    a = a -1;
                EndFor.
            EndWhile.
        EndBody."""
        expect = str()
        self.assertTrue(TestChecker.test(input,expect,495))
        
    def test_496(self):
        """Created automatically"""
        input = r"""
        Function: main
        Parameter: a[123], b, c[13][14][15]
        Body:
        Var: y;
            If a[12] > b Then
                Var: x;
                Do
                    a = b + 3; 
                    c[2][3] = int_of_float(c[4][2]+.10.2*.main(a,b,c))+a[2+int_of_float(main({2},a[3],a))+int_of_float(c[4])]; 
                While (x == y)  EndDo.
            EndIf.
        EndBody."""
        expect = str(TypeMismatchInStatement(Assign(Id("a"),BinaryOp("+",Id("b"),IntLiteral(3)))))
        self.assertTrue(TestChecker.test(input,expect,496))
        
    def test_497(self):
        """Created automatically"""
        input = r"""Function: main
            Parameter: a,b
            Body:
                a = "string 1";
                b = "string 2";
                Return a+b;
            EndBody. """
        expect = str(TypeMismatchInExpression(BinaryOp("+",Id("a"),Id("b"))))
        self.assertTrue(TestChecker.test(input,expect,497))
        
    def test_498(self):
        """Created automatically"""
        input = r"""Function: main
            Parameter: a,b
            Body:
                a[10e2] = (foo(x) +. 12.e3) *. 0x123 - a[b[2][3]] + 4;
            EndBody. """
        expect = str(TypeMismatchInExpression(ArrayCell(Id("a"),[FloatLiteral(1000.0)])))
        self.assertTrue(TestChecker.test(input,expect,498))
        
    def test_499(self):
        """Created automatically"""
        input = r""" 
            Function: main 
            Body:
                Var: x, y[1][3]={{{12,1}, {12., 12e3}},{23}, {13,32}};
                Var: b = True, c = False,i;
                For (i = 0, i < 10, 2) Do
                    For (i = 1, i < x*x , i + 1 ) Do
                    Var: a,z;
                    Var:j;
                        If(z && False) Then
                            Break;
                        ElseIf 1 Then
                            a=a-1;
                        EndIf.
                        For( j = 1, j < x*x ,j + 1) Do
                            Do
                                a = a * 1;
                            While( 1 ) 
                            EndDo.
                        EndFor.
                    EndFor.
                EndFor.
            EndBody.
            """
        expect = str(TypeMismatchInStatement(If([(BinaryOp("&&",Id("z"),BooleanLiteral(False)),[],[Break()]),(IntLiteral(1),[],[Assign(Id("a"),BinaryOp("-",Id("a"),IntLiteral(1)))])],([],[]))))
        self.assertTrue(TestChecker.test(input,expect,499))
        
    def test_500(self):
        """Created automatically"""
        input = r""" 
            Var: b;
                Function: main
                Body:
                    Var: a = 5,x;
                    a = a + foo(x);
                    b = 5.2;
                    Return 3;
                EndBody.

                Function: foo
                Parameter: a
                Body:
                    Var: c = 5;
                    Return c;
                EndBody.
            """
        expect = str(TypeCannotBeInferred(Assign(Id("a"),BinaryOp("+",Id("a"),CallExpr(Id("foo"),[Id("x")])))))
        self.assertTrue(TestChecker.test(input,expect,500))
        