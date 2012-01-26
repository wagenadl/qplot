// Range.H

#ifndef RANGE_H

#define RANGE_H

class Range {
public:
  Range();
  Range(double x);
  Range(double x, double y);
  bool empty() const;
  void extend(double x);
  void unionize(Range const &r);
  void intersect(Range const &r);
  bool contains(double x) const;
  double min() const { return min_; }
  double max() const { return max_; }
  double range() const;
private:
  double min_;
  double max_;
  bool empty_;
};

#endif
