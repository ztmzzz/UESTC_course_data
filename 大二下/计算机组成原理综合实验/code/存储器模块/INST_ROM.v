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
	 
	 assign ram[5'h00]=0;    				//
	 assign ram[5'h01]=32'h3c011234;    //lui R1,0x1234
	 assign ram[5'h02]=;    //lui R2,0x5678
	 assign ram[5'h03]=;    //add R3,R1,R2
	 assign ram[5'h04]=;    //sub R3,R1,R2
 	 assign ram[5'h05]=;    //and R3,R1,R2
	 assign ram[5'h06]=;    //or R3,R1,R2
	 assign ram[5'h07]=;    //xor R3,R1,R2
	 assign ram[5'h08]=;    //xor R3,R3,R3
	 assign ram[5'h09]=;    //sw R1,1(R3)
	 assign ram[5'h0a]=;    //lw R4,1(R3)
	 assign ram[5'h0b]=;    //beq R1,R2,0
	 assign ram[5'h0c]=;    //beq R1,R1,0xfffb

	 assign Inst=ram[addr[6:2]];

endmodule
