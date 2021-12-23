`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    20:31:06 06/23/2021 
// Design Name: 
// Module Name:    alu2 
// Project Name: 
// Target Devices: 
// Tool versions: 
// Description: 
//
// Dependencies: 
//
// Revision: 
// Revision 0.01 - File Created
// Additional Comments: 
//
//////////////////////////////////////////////////////////////////////////////////
module alu2(a,b,op,result,zero
    );
output [31:0] result;
output zero;
input [2:0] op;
input [31:0] a,b;
reg [31:0] result;
reg zero;
always@(*)
 begin
case(op)
	3'b000: result=a+b;
	3'b100: result=a-b;
	3'b001: result=a&b;				
	3'b101: result=a|b;
	3'b010: result=a^b;
	3'b110: result=b;
endcase
zero=(result==0)?1:0;
 end
endmodule