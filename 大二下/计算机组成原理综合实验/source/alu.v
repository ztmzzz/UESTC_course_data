`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    20:54:21 06/02/2021 
// Design Name: 
// Module Name:    alu 
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
module alu(a,b,op,result,zero
    );
output [31:0] result;
output zero;
input [3:0] op;
input [31:0] a,b;
reg [31:0] result;
reg zero;
always@(*)
 begin
case(op)
	4'b0000: result=a+b;
	4'b0100: result=a-b;
	4'b0001: result=a&b;				
	4'b0101: result=a|b;
	4'b0010: result=a^b;
	4'b0110: result=b;
endcase
zero=(result==0)?1:0;
 end
endmodule
