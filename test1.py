class A():
    def test(self):
        print("test")
class B(A):
    def test(self):
        print("B.test")
        super().test()
class C(B):
    def test(self):
        print("C.test")
        super().test()

a=C()
a.test()
