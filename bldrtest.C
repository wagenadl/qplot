#include <stdio.h>
#include <QString>
#include <QMap>

class Base {
public:
  Base() {
    printf("base\n");
  }
};

class Foo: public Base {
public:
  Foo() {
    printf("foo\n");
  }
};

class Bar: public Base {
public:
  Bar() {
    printf("bar\n");
  }
};


class BuilderBase {
public:
  static Base *build(QString x) {
    if (builders.contains(x))
      return builders[x]->build();
    else
      return 0;
  }
protected:
  virtual Base *build()=0;
  static QMap<QString, BuilderBase *> builders;
};

QMap<QString, BuilderBase *> BuilderBase::builders;

template <class X> class Builder: public BuilderBase {
public:
  Builder(char const *x) {
    printf("building %s\n", x);
    builders[x] = this;
  }
  Base *build() { return new X();
  }
};

Builder<Bar> barb("bar");
Builder<Foo> foob("foo");

int main() {
  printf("main\n");
  Base *b = BuilderBase::build("bar");
  printf("b = %p\n",b);
  Base *f = BuilderBase::build("foo");
  printf("f = %p\n",f);
  return 0;
}
