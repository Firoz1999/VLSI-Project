`include "4bitadder.v"
module eightbit(a,b,cin,sum,carry);
input [7:0] a,b;
input cin;
output [7:0] sum;
output carry;
wire [1:0] w;
fourbit FA0(a[3:0],b[3:0],cin,sum[3:0],w[0]);
fourbit FA1(a[7:4],b[7:4],w[0],sum[7:4],w[1]);
assign carry=w[1];
endmodule
