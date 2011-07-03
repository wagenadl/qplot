// Error.C

#include "Error.H"

#include <stdio.h>
#include <QDebug>

QTextStream *Error::dest = 0;

Error::Error(): QTextStream(&str, QIODevice::WriteOnly) {
}

Error::~Error() {
  if (dest)
    (*dest) << str << "\n";
  else {
    QTextStream ts(stderr, QIODevice::WriteOnly);
    ts << str << "\n";
  }
}

void Error::setDestination(QTextStream *d) {
  dest = d;
}
