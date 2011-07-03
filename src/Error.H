// Error.H

#ifndef ERROR_H

#define ERROR_H

#include <QTextStream>

class Error: public QTextStream {
public:
  Error();
  virtual ~Error();
  static void setDestination(QTextStream *);
private:
  QString str;
  static QTextStream *dest;
};

#endif
