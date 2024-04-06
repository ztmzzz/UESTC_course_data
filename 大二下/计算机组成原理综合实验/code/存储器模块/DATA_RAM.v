`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    12:09:36 11/12/2015 
// Design Name: 
// Module Name:    DATA_RAM 
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
module DATA_RAM(
		input        Clock,
		output[31:0] dataout,
		input [31:0] datain,
		input [31:0] addr,
		input        write , read
    );

   reg [31:0] ram [0:31];
	
	assign dataout = read ? ram[addr[6:2]] : 32'hxxxxxxxx;
	
	always @ (posedge Clock) begin
			if (write) ram[addr[6:2]] = datain;
	end

	integer i;
	
	initial begin
			for ( i = 0 ; i <= 31 ; i = i + 1) ram [i] = i * i;
	end		

endmodule
