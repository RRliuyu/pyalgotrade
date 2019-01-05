class A():
    def test(self):
        print("test")
class B(A):
    def test(self):
        print("B.test")
        super().test()

a=B()
a.test()
