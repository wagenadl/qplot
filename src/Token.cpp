// Token.C

#include "Token.H"

Token::Token() {
  typ = NONE;
  num = 0;
  str = "";
}

Token::Token(Token::Type t) {
  typ = t;
  num = 0;
  str = "<" + QString::number(int(t)) + ">";
}

Token::Token(double n) {
  typ = NUMBER;
  num = n;
  str = "#" + QString::number(n);
}

Token::Token(Token::Type t, QString s) {
  typ = t;
  str = s;
}
