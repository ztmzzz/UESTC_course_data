`timescale 1ns / 1ps

////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer:
//
// Create Date:   22:32:17 06/25/2021
// Design Name:   RegFile
// Module Name:   C:/Users/Administrator/Desktop/111/bbb/regfiletest.v
// Project Name:  bbb
// Target Device:  
// Tool versions:  
// Description: 
//
// Verilog Test Fixture created by ISE for module: RegFile
//
// Dependencies:
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
////////////////////////////////////////////////////////////////////////////////

module regfiletest;

	// Inputs
	reg [4:0] Rn1;
	reg [4:0] Rn2;
	reg [4:0] Wn;
	reg Write;
	reg [31:0] Wd;
	reg Clock;

	// Outputs
	wire [31:0] A;
	wire [31:0] B;

	// Instantiate the Unit Under Test (UUT)
	RegFile uut (
		.Rn1(Rn1), 
		.Rn2(Rn2), 
		.Wn(Wn), 
		.Write(Write), 
		.Wd(Wd), 
		.A(A), 
		.B(B), 
		.Clock(Clock)
	);

	initial begin
		// Initialize Inputs
		Rn1 = 0;
		Rn2 = 0;
		Wn = 0;
		Write = 0;
		Wd = 0;
		Clock = 0;

		// Wait 100 ns for global reset to finish
		#100;Clock = 0;Wn=4'b0001;Write=1;Wd=32'hFFFFFFFF;
      #100;Clock = 1;
		#100;Clock = 0;
      #100;Clock = 1;
		#100;Clock = 0;Write=0;Rn1=4'b0001;
      #100;Clock = 1;
		#100;Clock = 0;
      #100;Clock = 1;
		#100;Clock = 0;
      #100;Clock = 1;
		#100;Clock = 0;
      #100;Clock = 1;
		// Add stimulus here

	end
      
endmodule

