// Token.C

#include "Token.H"

Token::Token() {
  typ = NONE;
}

Token::Token(Token::Type t) {
  typ = t;
}

Token::Token(double n) {
  typ = NUMBER;
  num = n;
}

Token::Token(Token::Type t, QString s) {
  typ = t;
  str = s;
}
