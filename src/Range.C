// Range.C

#include "Range.H"

Range::Range() {
  empty_ = true;
}

Range::Range(double x) {
  min_ = max_ = x;
  empty_ = false;
}

Range::Range(double x, double y) {
  min_ = max_ = x;
  empty_ = false;
  extend(y);
}

bool Range::empty() const {
  return empty_;
}

void Range::extend(double x) {
  if (empty_) {
    min_ = max_ = x;
    empty_ = false;
  } else {
    if (x<min_)
      min_=x;
    if (x>max_)
      max_=x;
  }
}

void Range::unionize(Range const &r) {
  if (r.empty_)
    return;
  if (empty_) {
    min_ = r.min_;
    max_ = r.max_;
    empty_ = false;
  } else {
    if (r.min_<min_)
      min_ = r.min_;
    if (r.max_>max_)
      max_ = r.max_;
  }
}

void Range::intersect(Range const &r) {
  if (empty_)
    return;
  if (r.empty_) {
    empty_ = true;
  } else {
    if (r.min_>min_)
      min_ = r.min_;
    if (r.max_<max_)
      max_ = r.max_;
    if (min_>max_)
      empty_ = true;
  }
}

bool Range::contains(double x) const {
  if (empty_)
    return false;
  else
    return x>=min_ && x<=max_;
}

double Range::range() const {
  if (empty_)
    return 0;
  else
    return max_ - min_;
}
