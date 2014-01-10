// CmdPanel.C

#include "CmdPanel.H"


static CBuilder<CmdPanel> cbPanel("panel");

bool CmdPanel::usage() {
  return error("Usage: panel ID [x y w h] | -");
}

bool CmdPanel::parse(Statement const &s) {
  if (s.length()==2 && s[1].typ==Token::DASH)
    return true;
  else if (s.length()==2 &&
	   (s[1].typ==Token::CAPITAL || s[1].typ==Token::BAREWORD))
    return true;
  else if (s.length()==2+4 &&
	   (s[1].typ==Token::CAPITAL || s[1].typ==Token::BAREWORD) &&
	   s[2].typ==Token::NUMBER &&
	   s[3].typ==Token::NUMBER &&
	   s[4].typ==Token::NUMBER &&
	   s[5].typ==Token::NUMBER)
    return true;
  else
    return usage();
}


void CmdPanel::render(Statement const &s, Figure &f, bool dryrun) {
  f.leavePanel();
  if (s[1].typ==Token::DASH)
    return;
  
  QRectF area;
  if (s.length()==6) {
    area = QRectF(pt2iu(s[2].num), pt2iu(s[3].num),
		  pt2iu(s[4].num), pt2iu(s[5].num));
    if (!dryrun)
      f.painter().drawRect(area);
  }
  f.choosePanel(s[1].str);
  if (s.length()==6)
    f.setExtent(area);
}
