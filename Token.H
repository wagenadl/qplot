// Token.H

#ifndef TOKEN_H

#define TOKEN_H

#include <QString>

struct Token {
  enum Type {
    NONE,
    BAREWORD,
    CAPITAL,
    NUMBER,
    OPENBRACKET,
    CLOSEBRACKET,
    OPENPAREN,
    CLOSEPAREN,
    STRING,
    DASH,
    DATAREF,
  };
  Type typ;
  double num;
  QString str;
public:
  Token();
  Token(Type typ);
  Token(double num);
  Token(Type typ, QString str);
};

#endif
