// CmdYlim.C

#include "CmdYLim.H"


static CBuilder<CmdYLim> cbYLim("ylim");

bool CmdYLim::usage() {
  return error("Usage: ylim y0 y1");
}

bool CmdYLim::parse(Statement const &s) {
  if (s.length()==3 && s[1].typ==Token::NUMBER && s[2].typ==Token::NUMBER)
    return true;
  else
    return usage();
}


void CmdYLim::render(Statement const &s, Figure &f, bool) {
  double x0 = s[1].num;
  double x1 = s[2].num;
  f.yAxis().setDataRange(x0, x1);
}
