# 2024/12/2

This was a fun one! Regex!

My input had a `mul` as index zero on one of the lines, very clever. I had set my default `do_position` to be `0`, and inevitably this came around to bite me. Using `0` as a magic number is not advised.
