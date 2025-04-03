#include <iostream>
using namespace std;

class A {
public:
    A() {
        std::cout << "A()" << std::endl;
    }
    ~A() {
        std::cout << "~A()" << std::endl;
    }
    virtual void print() {
        std::cout << "A::print()" << std::endl;
    }
};

class B : public A {
public:
    B() {
        std::cout << "B()" << std::endl;
    }
    ~B() {
        std::cout << "~B()" << std::endl;
    }
    virtual void print() override {
        std::cout << "B::print()" << std::endl;
    }
};

class C : public A {
public:
    C() {
        std::cout << "C()" << std::endl;
    }
    ~C() {
        std::cout << "~C()" << std::endl;
    }
    virtual void print() override {
        std::cout << "C::print()" << std::endl;
    }
};

int main(){
  class A *a = new B();
  cout << "Made a B" << endl;
  a->print();
}
