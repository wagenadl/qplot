// CmdCumul.C

#include "CmdCumul.H"
#include <QDebug>

static CBuilder<CmdCumul> cbCumul("cumul");

bool CmdCumul::usage() {
  return error("Usage: cumul\n");
}

bool CmdCumul::parse(Statement const &s) {
  if (s.length()==1)
    return true;
  else
    return usage();
}

void CmdCumul::render(Statement const &, Figure &f, bool) {
  f.clearBBox();
}

