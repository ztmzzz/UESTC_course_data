`timescale 1ns / 1ps

////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer:
//
// Create Date:   20:39:29 06/02/2021
// Design Name:   extnd
// Module Name:   D:/111/aaa/extndtest.v
// Project Name:  aaa
// Target Device:  
// Tool versions:  
// Description: 
//
// Verilog Test Fixture created by ISE for module: extnd
//
// Dependencies:
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
////////////////////////////////////////////////////////////////////////////////

module extndtest;

	// Inputs
	reg [15:0] data_16bit;

	// Outputs
	wire [31:0] data_32bit;

	// Instantiate the Unit Under Test (UUT)
	extnd uut (
		.data_32bit(data_32bit), 
		.data_16bit(data_16bit)
	);

	initial begin
		// Initialize Inputs
		data_16bit = 0;

		// Wait 100 ns for global reset to finish
		#100;data_16bit=16'hFFFF;
		#100;data_16bit=16'h00AA;
        
		// Add stimulus here

	end
      
endmodule

