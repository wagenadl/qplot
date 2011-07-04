// CmdEndGroup.C

#include "CmdEndGroup.H"
#include <QDebug>

static CBuilder<CmdEndGroup> cbEndGroup("endgroup");

bool CmdEndGroup::usage() {
  return error("Usage: endgroup\n");
}

bool CmdEndGroup::parse(Statement const &s) {
  if (s.length()==1)
    return true;
  else
    return usage();
}

void CmdEndGroup::render(Statement const &, Figure &f, bool) {
  f.endGroup();
}

