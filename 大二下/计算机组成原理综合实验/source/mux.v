`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    20:26:01 06/16/2021 
// Design Name: 
// Module Name:    mux 
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
module mux(a,b,c,z
    );
input [31:0] a,b;
input c;
output [31:0] z;
reg [31:0] z;
always @(*)
case(c)
	1'b1:z<=b;
	1'b0:z<=a;
endcase
endmodule
