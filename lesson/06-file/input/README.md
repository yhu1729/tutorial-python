# Synthetic motion measurements

`measurement.csv` was created for this course, not collected from an instrument.
Its five rows follow the exact formula $x(t)=1+2t$ at $t=0,1,2,3,4$.
`time_s` is time in seconds; `position_m` is position in metres.
The initial position is 1 m and the velocity is 2 m/s.
There is no noise, uncertainty model, missing data, or experimental provenance.
These data allow exact checks of reading, averaging, and unit conversion.

The reader requires the header `time_s,position_m` in this order, exactly two
fields per row, at least one data row, and finite numeric values.
Time ordering is deliberately not part of this file-reading contract: this
lesson computes a mean, not a derivative or trajectory interpolation.
