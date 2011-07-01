// CmdXLim.C

#include "CmdXLim.H"


static CBuilder<CmdXLim> cbXLim("xlim");

bool CmdXLim::usage() {
  return error("Usage: xlim x0 x1");
}

bool CmdXLim::parse(Statement const &s) {
  if (s.length()==3 && s[1].typ==Token::NUMBER && s[2].typ==Token::NUMBER)
    return true;
  else
    return usage();
}


void CmdXLim::render(Statement const &s, Figure &f, bool) {
  double x0 = s[1].num;
  double x1 = s[2].num;
  f.xAxis().setDataRange(x0, x1);
}
