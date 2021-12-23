`timescale 1ns / 1ps

////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer:
//
// Create Date:   23:51:59 06/25/2021
// Design Name:   cpu
// Module Name:   C:/Users/Administrator/Desktop/111/bbb/cputest.v
// Project Name:  bbb
// Target Device:  
// Tool versions:  
// Description: 
//
// Verilog Test Fixture created by ISE for module: cpu
//
// Dependencies:
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
////////////////////////////////////////////////////////////////////////////////

module cputest;

	// Inputs
	reg Clock;
	reg Reset;

	// Outputs
	wire [31:0] addr;
	wire [31:0] result;

	// Instantiate the Unit Under Test (UUT)
	cpu uut (
		.Clock(Clock), 
		.Reset(Reset), 
		.addr(addr), 
		.result(result)
	);

	initial begin
		// Initialize Inputs
		Clock = 0;
		Reset = 0;

		// Wait 100 ns for global reset to finish
		#100;Clock = 0;
      #100;Clock = 1;
		#100;Clock = 0;Reset=1;
      #100;Clock = 1;
		#100;Clock = 0;
      #100;Clock = 1;
		#100;Clock = 0;
      #100;Clock = 1;
		#100;Clock = 0;
      #100;Clock = 1;
		#100;Clock = 0;
      #100;Clock = 1;
		#100;Clock = 0;
      #100;Clock = 1;
		#100;Clock = 0;
      #100;Clock = 1;
		#100;Clock = 0;
      #100;Clock = 1;
		#100;Clock = 0;
      #100;Clock = 1;
		#100;Clock = 0;
      #100;Clock = 1;
		#100;Clock = 0;
      #100;Clock = 1;
		#100;Clock = 0;
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

