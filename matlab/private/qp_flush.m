function qp_flush(fd)
global qp_data
if qp_data.isoctave
  fflush(fd);
end
