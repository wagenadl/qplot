// CmdFont.C

#include "CmdFont.H"


static CBuilder<CmdFont> cbFont("font");

bool CmdFont::usage() {
  return error("Usage: font family [bold] [italic] size");
}

bool CmdFont::parse(Statement const &s) {
  if (s.length()<3 || s.length()>5)
    return usage();
  if (s[1].typ!=Token::BAREWORD)
    return usage();
  if (s[s.length()-1].typ!=Token::NUMBER)
    return usage();
  for (int k=2; k<s.length()-1; k++) {
    if (s[k].typ==Token::BAREWORD) {
      if (s[k].str=="bold")
	continue;
      else if (s[k].str=="italic")
	continue;
    }
    return usage();
  }
  return true;
}


void CmdFont::render(Statement const &s, Figure &f, bool) {
  QFont font(s[1].str);
  //  font.setPointSizeF(pt2iu(s[s.length()-1].num));
  font.setPixelSize(pt2iu(s[s.length()-1].num));
  for (int k=2; k<s.length()-1; k++) {
    if (s[k].str=="bold")
      font.setWeight(QFont::Bold);
    else if (s[k].str=="italic")
      font.setItalic(true);
  }
  f.painter().setFont(font);
}
