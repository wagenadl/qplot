// CmdFigSize.C

#include "CmdFigSize.H"


static CBuilder<CmdFigSize> cbFigSize("figsize");

bool CmdFigSize::usage() {
  return error("Usage: figsize width_pt height_pt");
}

bool CmdFigSize::parse(Statement const &s) {
  if (s.length()==3 && s[1].typ==Token::NUMBER && s[2].typ==Token::NUMBER)
    return true;
  else
    return usage();
}


void CmdFigSize::render(Statement const &s, Figure &f, bool) {
  double w = s[1].num;
  double h = s[2].num;
  f.setSize(QSizeF(w,h));
}
