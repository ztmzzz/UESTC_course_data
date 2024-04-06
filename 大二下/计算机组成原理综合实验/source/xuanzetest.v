`timescale 1ns / 1ps

////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer:
//
// Create Date:   20:25:05 06/02/2021
// Design Name:   xuanze
// Module Name:   D:/111/aaa/xuanzetest.v
// Project Name:  aaa
// Target Device:  
// Tool versions:  
// Description: 
//
// Verilog Test Fixture created by ISE for module: xuanze
//
// Dependencies:
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
////////////////////////////////////////////////////////////////////////////////

module xuanzetest;

	// Inputs
	reg [31:0] in1;
	reg [31:0] in2;
	reg sel;

	// Outputs
	wire [31:0] out_data;

	// Instantiate the Unit Under Test (UUT)
	xuanze uut (
		.out_data(out_data), 
		.in1(in1), 
		.in2(in2), 
		.sel(sel)
	);

	initial begin
		// Initialize Inputs
		in1 = 0;
		in2 = 0;
		sel = 0;

		// Wait 100 ns for global reset to finish
		#100;in1=32'hFFFFFFFF;in2=32'h00000000;sel=0;
		#100;in1=32'hFFFF0000;in2=32'h00000000;sel=0;
      #100;in1=32'hFFFFFFFF;in2=32'h00000000;sel=1;
		#100;in1=32'hFFFFFFFF;in2=32'h0000FFFF;sel=1;
		// Add stimulus here

	end
      
endmodule

