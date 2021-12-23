`timescale 1ns / 1ps

////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer:
//
// Create Date:   21:14:53 06/16/2021
// Design Name:   fetch
// Module Name:   D:/111/aaa/fetchtest.v
// Project Name:  aaa
// Target Device:  
// Tool versions:  
// Description: 
//
// Verilog Test Fixture created by ISE for module: fetch
//
// Dependencies:
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
////////////////////////////////////////////////////////////////////////////////

module fetchtest;

	// Inputs
	reg clk;
	reg rst;
	reg [31:0] b_addr;
	reg z;
	reg b;

	// Outputs
	wire [31:0] addr;

	// Instantiate the Unit Under Test (UUT)
	fetch uut (
		.clk(clk), 
		.rst(rst), 
		.b_addr(b_addr), 
		.z(z), 
		.b(b), 
		.addr(addr)
	);

	initial begin
		// Initialize Inputs
		clk = 0;
		rst = 0;
		b_addr = 0;
		z = 0;
		b = 0;
		
		// Wait 100 ns for global reset to finish
		#100;clk=0;rst=0;b_addr=32'h00000001;
		#100;clk=1;
		#100;clk=0;b=1;z=1;rst=1;
      #100;clk=1;  
		#100;clk=0;b=0;z=1;
      #100;clk=1;  
		#100;clk=0;b=1;z=0;
      #100;clk=1;
		// Add stimulus here

	end
      
endmodule

