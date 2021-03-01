`include "16bitadder.v"
module thirtytwobit(a,b,cin,sum,carry);
input [31:0] a,b;
input cin;
output [31:0] sum;
output carry;
wire [1:0] w;
sixteenbit FA0(a[15:0],b[15:0],cin,sum[15:0],w[0]);
sixteenbit FA1(a[31:16],b[31:16],w[0],sum[31:16],w[1]);
assign carry=w[1];
endmodule
