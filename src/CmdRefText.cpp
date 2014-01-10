// CmdReftext.C

#include "CmdRefText.H"
#include <QFontMetricsF>
#include "Rotate.H"
#include <QDebug>

static CBuilder<CmdRefText> cbRefText("reftext");

bool CmdRefText::usage() {
  return error("Usage: reftext [string]");
}

bool CmdRefText::parse(Statement const &s) {
  if (s.length()==2 && s[1].typ==Token::STRING)
    return true;
  else if (s.length()==1)
    return true;
  else
    return usage();
}

void CmdRefText::render(Statement const &s, Figure &f, bool) {
  if (s.length()==1)
    f.setRefText("");
  else
    f.setRefText(s[1].str);
}
