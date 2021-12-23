`timescale 1ns / 1ps

////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer:
//
// Create Date:   20:25:37 06/23/2021
// Design Name:   aluop
// Module Name:   D:/111/aaa/aluoptest.v
// Project Name:  aaa
// Target Device:  
// Tool versions:  
// Description: 
//
// Verilog Test Fixture created by ISE for module: aluop
//
// Dependencies:
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
////////////////////////////////////////////////////////////////////////////////

module aluoptest;

	// Inputs
	reg [1:0] aluctr;
	reg [5:0] func;

	// Outputs
	wire [2:0] aluop;

	// Instantiate the Unit Under Test (UUT)
	aluop uut (
		.aluctr(aluctr), 
		.func(func), 
		.aluop(aluop)
	);

	initial begin
		// Initialize Inputs
		aluctr = 0;
		func = 0;

		// Wait 100 ns for global reset to finish
		#100;aluctr=2'b10;func=6'b100000;
      #200;aluctr=2'b01;func=6'b100000;
		// Add stimulus here

	end
      
endmodule

