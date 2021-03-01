`include "32bitadder.v"
module sixtyfourbit(a,b,cin,sum,carry);
input [63:0] a,b;
input cin;
output [63:0] sum;
output carry;
wire [1:0] w;
thirtytwobit FA0(a[31:0],b[31:0],cin,sum[31:0],w[0]);
thirtytwobit FA1(a[63:32],b[63:32],w[0],sum[63:32],w[1]);
assign carry=w[1];
endmodule

module top;
wire [63:0]sum;
wire carry;
reg [63:0]a, b;
reg c;
sixtyfourbit bit(a, b, c, sum, carry);
initial
begin
#0  c=1'b0;
if($value$plusargs("a=%b",a) && $value$plusargs("b=%b",b));
end

initial
begin
	$monitor("%b",sum);

end

endmodule
