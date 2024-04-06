`timescale 1ns / 1ps

////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer:
//
// Create Date:   20:20:54 06/23/2021
// Design Name:   control
// Module Name:   D:/111/aaa/controltest.v
// Project Name:  aaa
// Target Device:  
// Tool versions:  
// Description: 
//
// Verilog Test Fixture created by ISE for module: control
//
// Dependencies:
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
////////////////////////////////////////////////////////////////////////////////

module controltest;

	// Inputs
	reg [5:0] func;
	reg [5:0] op;

	// Outputs
	wire regdst;
	wire regw;
	wire alusrc;
	wire [2:0] aluop;
	wire memw;
	wire memr;
	wire memtoreg;
	wire branch;

	// Instantiate the Unit Under Test (UUT)
	control uut (
		.func(func), 
		.op(op), 
		.regdst(regdst), 
		.regw(regw), 
		.alusrc(alusrc), 
		.aluop(aluop), 
		.memw(memw), 
		.memr(memr), 
		.memtoreg(memtoreg), 
		.branch(branch)
	);

	initial begin
		// Initialize Inputs
		func = 0;
		op = 0;

		// Wait 100 ns for global reset to finish
		#100;op=6'b000000;func=6'b100000;
		#100;op=6'b000000;func=6'b100010;
		#100;op=6'b000000;func=6'b100100;
		#100;op=6'b000000;func=6'b100101;
		#100;op=6'b000000;func=6'b100110;
		#100;op=6'b100011;
		#100;op=6'b101011;
		#100;op=6'b000100;
		#100;op=6'b001111;
        
		// Add stimulus here

	end
      
endmodule

