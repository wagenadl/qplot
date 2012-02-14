// CmdHairline.C

#include "CmdHairline.H"

static CBuilder<CmdHairline> cbHairline("hairline");

bool CmdHairline::usage() {
  return error("Usage: hairline width");
}

bool CmdHairline::parse(Statement const &s) {
  if (s.length()==2 && s[1].typ==Token::NUMBER)
    return true;
  else
    return usage();
}


void CmdHairline::render(Statement const &s, Figure &f, bool) {
  f.setHairline(s[1].num);
}
