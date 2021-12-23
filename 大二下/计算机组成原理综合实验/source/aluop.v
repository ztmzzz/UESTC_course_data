`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    19:35:23 06/23/2021 
// Design Name: 
// Module Name:    aluop 
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
module aluop(aluctr,func,aluop
    );
input [1:0] aluctr;
input [5:0] func;
output [2:0] aluop;
reg [2:0] aluop;

always @(*)
	case(aluctr)
		2'b10:	case(func)
						6'b100000:aluop=3'b000;
						6'b100010:aluop=3'b100;
						6'b100100:aluop=3'b001;
						6'b100101:aluop=3'b101;
						6'b100110:aluop=3'b010;
					endcase
		2'b00:aluop=3'b000;
		2'b01:aluop=3'b100;
		2'b11:aluop=3'b110;
	endcase
endmodule
