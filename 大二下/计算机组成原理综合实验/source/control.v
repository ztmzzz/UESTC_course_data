`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    19:27:59 06/23/2021 
// Design Name: 
// Module Name:    control 
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
module control(func,op,regdst,regw,alusrc,aluop,memw,memr,memtoreg,branch
    );
input [5:0] op,func;
output [2:0] aluop;
output regdst,regw,alusrc,memw,memr,memtoreg,branch;
reg regdst,regw,alusrc,memw,memr,memtoreg,branch;
wire [2:0] aluop;
reg [1:0] aluctr;
always @(*)
	case(op)
		6'b000000:begin
						regdst=1'b1;
						regw=1'b1;
						alusrc=1'b0;
						memw=1'b0;
						memr=1'b0;
						memtoreg=1'b0;
						branch=1'b0;
						aluctr=2'b10;
					 end
		6'b100011:begin
						regdst=1'b0;
						regw=1'b1;
						alusrc=1'b1;
						memw=1'b0;
						memr=1'b1;
						memtoreg=1'b1;
						branch=1'b0;
						aluctr=2'b00;
					 end
		6'b101011:begin
						regdst=1'bx;
						regw=1'b0;
						alusrc=1'b1;
						memw=1'b1;
						memr=1'b0;
						memtoreg=1'bx;
						branch=1'b0;
						aluctr=2'b00;
					 end
		6'b000100:begin
						regdst=1'bx;
						regw=1'b0;
						alusrc=1'b0;
						memw=1'b0;
						memr=1'b0;
						memtoreg=1'bx;
						branch=1'b1;
						aluctr=2'b01;
					 end
		6'b001111:begin
						regdst=1'b0;
						regw=1'b1;
						alusrc=1'b1;
						memw=1'b0;
						memr=1'b0;
						memtoreg=1'b0;
						branch=1'b0;
						aluctr=2'b11;
					 end
	endcase
aluop u1(.aluctr(aluctr),.func(func),.aluop(aluop));
endmodule
