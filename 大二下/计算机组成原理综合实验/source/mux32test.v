`timescale 1ns / 1ps

////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer:
//
// Create Date:   22:04:31 06/25/2021
// Design Name:   mux32
// Module Name:   C:/Users/Administrator/Desktop/111/bbb/mux32test.v
// Project Name:  bbb
// Target Device:  
// Tool versions:  
// Description: 
//
// Verilog Test Fixture created by ISE for module: mux32
//
// Dependencies:
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
////////////////////////////////////////////////////////////////////////////////

module mux32test;

	// Inputs
	reg [31:0] A;
	reg [31:0] B;
	reg sel;

	// Outputs
	wire [31:0] out;

	// Instantiate the Unit Under Test (UUT)
	mux32 uut (
		.A(A), 
		.B(B), 
		.sel(sel), 
		.out(out)
	);

	initial begin
		// Initialize Inputs
		A = 0;
		B = 0;
		sel = 0;

		// Wait 100 ns for global reset to finish
		#100;A=32'hFFFFFFFF;B=32'h00000000;
		#100;sel=1;
		#100;sel=0;
        
		// Add stimulus here

	end
      
endmodule

