// CmdAlign.C

#include "CmdAlign.H"


static CBuilder<CmdAlign> cbAlign("align");

bool CmdAlign::usage() {
  return error("Usage: align left|right|center|top|bottom|middle|base ...");
}

static int halignment(QString s) {
  if (s=="left")
    return Figure::LEFT;
  else if (s=="right")
    return Figure::RIGHT;
  else if (s=="center")
    return Figure::CENTER;
  else
    return -1;
}

static int valignment(QString s) {
  if (s=="top")
    return Figure::TOP;
  else if (s=="bottom")
    return Figure::BOTTOM;
  else if (s=="middle")
    return Figure::MIDDLE;
  else if (s=="base")
    return Figure::BASE;
  else
    return -1;
}

bool CmdAlign::parse(Statement const &s) {
  if (s.length()<2)
    return usage();
  for (int k=1; k<s.length(); k++) {
    if (s[k].typ==Token::BAREWORD) {
      if (valignment(s[k].str)>=0)
	continue;
      else if (halignment(s[k].str)>=0)
	continue;
    }
    return usage();
  }
  return true;
}


void CmdAlign::render(Statement const &s, Figure &f, bool) {
  for (int k=1; k<s.length(); k++) {
    if (halignment(s[k].str)>=0)
      f.setHAlign(Figure::HAlign(halignment(s[k].str)));
    else if (valignment(s[k].str)>=0)
      f.setVAlign(Figure::VAlign(valignment(s[k].str)));
  }
}
