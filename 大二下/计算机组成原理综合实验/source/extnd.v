`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    20:30:29 06/02/2021 
// Design Name: 
// Module Name:    extnd 
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
module extnd(data_32bit,data_16bit
    );
input [15:0] data_16bit;
output [31:0] data_32bit;

assign data_32bit=data_16bit[15] ? {16'hFFFF,data_16bit} : {16'h0000,data_16bit};

endmodule
