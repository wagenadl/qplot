// CmdAt.C

#include "CmdAt.H"


static CBuilder<CmdAt> cbAt("at");

bool CmdAt::usage() {
  return error("Usage: at x y [dx dy]");
}

bool CmdAt::parse(Statement const &s) {
  if (s.length()==3 || s.length()==5) {
    for (int k=1; k<s.length(); k++)
      if (s[1].typ!=Token::NUMBER)
	return usage();
    return true;
  } else {
    return usage();
  }
}


void CmdAt::render(Statement const &s, Figure &f, bool) {
  double x = s[1].num;
  double y = s[2].num;
  if (s.length()==5) {
    double dx = s[3].num;
    double dy = s[4].num;
    f.setAnchor(x,y, dx,dy);
  } else {
    f.setAnchor(x,y);
  }
}
