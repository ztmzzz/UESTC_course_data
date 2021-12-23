`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    20:38:12 06/16/2021 
// Design Name: 
// Module Name:    fetch 
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
module fetch(clk,rst,b_addr,z,b,addr
    );
input clk,rst,b,z;
input [31:0] b_addr;
output [31:0] addr;

wire zb;
wire [31:0] muxout;
wire [31:0] add2in;
wire [31:0] add1out;
wire [31:0] add2out;
and2 u1(.a(z),.b(b),.out(zb));
extnd2 u3(.a(b_addr),.b(add2in));
add add1(.a(addr),.b(32'b100),.out(add1out));
add add2(.a(add1out),.b(add2in),.out(add2out));
mux32 u4(.A(add1out),.B(add2out),.sel(zb),.out(muxout));
pc u2(.clk(clk),.rst(rst),.d(muxout),.pc(addr));
endmodule
