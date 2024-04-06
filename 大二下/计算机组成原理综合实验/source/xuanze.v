`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    20:20:58 06/02/2021 
// Design Name: 
// Module Name:    xuanze 
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
module xuanze(out_data,in1,in2,sel
    );
input [31:0] in1,in2;
input sel;
output [31:0] out_data;
reg [31:0] out_data;
always@(in1,in2,sel)
	if(!sel) out_data=in1;
	else out_data=in2;	

endmodule
