`include "HalfAdder.v"
module full_adder(a,b,c,sum, carry);
input a, b, c;
output sum, carry;
wire half_sum_1, half_carry_1, half_carry_2;
HalfAdder HA1(a,b,half_sum_1, half_carry_1);
HalfAdder HA2( half_sum_1, c,sum, half_carry_2);
assign carry=half_carry_1 | half_carry_2;
endmodule
