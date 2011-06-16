// Error.C

#include "Error.H"

#include <stdio.h>

Error::Error(): QTextStream(stderr, QIODevice::WriteOnly) {
}

Error::~Error() {
  (*this) << "\n";
}
