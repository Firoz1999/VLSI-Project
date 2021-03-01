`include "8bitadder.v"
module sixteenbit(a,b,cin,sum,carry);
input [15:0] a,b;
input cin;
output [15:0] sum;
output carry;
wire [1:0] w;
eightbit FA0(a[7:0],b[7:0],cin,sum[7:0],w[0]);
eightbit FA1(a[15:8],b[15:8],w[0],sum[15:8],w[1]);
assign carry=w[1];
endmodule

