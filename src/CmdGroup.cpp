// CmdGroup.C

#include "CmdGroup.H"
#include <QDebug>

static CBuilder<CmdGroup> cbGroup("group");

bool CmdGroup::usage() {
  return error("Usage: group\n");
}

bool CmdGroup::parse(Statement const &s) {
  if (s.length()==1)
    return true;
  else
    return usage();
}

void CmdGroup::render(Statement const &, Figure &f, bool) {
  f.startGroup();
}

