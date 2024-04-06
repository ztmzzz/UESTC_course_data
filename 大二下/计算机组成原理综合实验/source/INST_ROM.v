`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    19:35:57 12/17/2017 
// Design Name: 
// Module Name:    INST_ROM 
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
module INST_ROM(
	 input [31:0] addr,
	 output [31:0] Inst
    );
	 
	 wire [31:0] ram [31:0];
	 
	 assign ram[5'h00]=32'h3c011111;    //lui R1,0x1111
	 assign ram[5'h01]=32'h3c022222;    //lui R2,0x2222
	 assign ram[5'h02]=32'h00221820;    //add R3,R1,R2;R3=0x3333
	 assign ram[5'h03]=32'h00412022;    //sub R4,R2,R1;R4=0x1111
	 assign ram[5'h04]=32'h00222824;    //and R5,R1,R2
 	 assign ram[5'h05]=32'h00233025;    //or R6,R1,R3
	 assign ram[5'h06]=32'h00243826;    //xor R7,R1,R4;R7=0x0000;
	 assign ram[5'h07]=32'h3c080001;    //lui R8,0x0001;
	 assign ram[5'h08]=32'had030001;    //sw R3,1(R8);s2=R3;
	 assign ram[5'h09]=32'h8ce90002;    //lw R9,2(R7);R9=s2;
	 assign ram[5'h0a]=32'h10220001;    //beq R1,R2,0x0001;pc+1;not equal
	 assign ram[5'h0b]=32'h11230001;    //beq R9,R3,0x0001;pc+2;equal
	 assign ram[5'h0c]=32'h3c0a000f;    //lui R10,0x000F;
	 assign ram[5'h0d]=32'h3c0a00ff;    //lui R10,0x00FF;

	 assign Inst=ram[addr[6:2]];

endmodule
