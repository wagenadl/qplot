// CmdFigSize.C

#include "CmdFigSize.H"


static CBuilder<CmdFigSize> cbFigSize("figsize");

bool CmdFigSize::usage() {
  return error("Usage:\n  figsize width_pt height_pt\n");
}

bool CmdFigSize::parse(Statement const &s) {
  if (s.length()==3 && s[1].typ==Token::NUMBER && s[2].typ==Token::NUMBER)
    return true;
  else
    return usage();
}


QRectF CmdFigSize::bounds(Statement const &s, Figure &f) {
  double w = s[1].num;
  double h = s[2].num;
  f.setSize(QSizeF(w,h));
  return QRectF();
}

void CmdFigSize::render(Statement const &, Figure &) {
}
