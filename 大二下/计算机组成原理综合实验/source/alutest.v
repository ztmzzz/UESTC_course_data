`timescale 1ns / 1ps

////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer:
//
// Create Date:   21:13:04 06/02/2021
// Design Name:   alu
// Module Name:   D:/111/aaa/alutest.v
// Project Name:  aaa
// Target Device:  
// Tool versions:  
// Description: 
//
// Verilog Test Fixture created by ISE for module: alu
//
// Dependencies:
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
////////////////////////////////////////////////////////////////////////////////

module alutest;

	// Inputs
	reg [31:0] a;
	reg [31:0] b;
	reg [3:0] op;

	// Outputs
	wire [31:0] result;
	wire zero;

	// Instantiate the Unit Under Test (UUT)
	alu uut (
		.a(a), 
		.b(b), 
		.op(op), 
		.result(result), 
		.zero(zero)
	);

	initial begin
		// Initialize Inputs
		a = 0;
		b = 0;
		op = 0;

		// Wait 100 ns for global reset to finish
		#100;a=32'hABCD;b=32'hABCD;op=4'b0100;
		#100;a=32'h0C0C;b=32'hABCD;op=4'b0000;
		#100;a=32'h0C0C;b=32'hABCD;op=4'b0001;
		#100;a=32'h0C0C;b=32'hABCD;op=4'b0101;
		#100;a=32'h0C0C;b=32'hABCD;op=4'b0010;
		#100;a=32'h0C0C;b=32'hABCD;op=4'b0110;
        
		// Add stimulus here

	end
      
endmodule

