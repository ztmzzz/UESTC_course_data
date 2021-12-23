`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    20:58:43 06/23/2021 
// Design Name: 
// Module Name:    cpu 
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
module cpu(Clock,Reset,addr,result
    );
input Clock,Reset;
output [31:0] addr,result;

wire zero,branch,regdst,regw,alusrc,memw,memr,memtoreg;
wire [31:0] inst,Wd,A,B,aluB,imm32,dataout;
wire [2:0] aluop;
wire [4:0] Wn;

fetch u1(.clk(Clock),.rst(Reset),.b_addr(imm32),.z(zero),.b(branch),.addr(addr));
INST_ROM u2(.addr(addr),.Inst(inst));
control u3(.func(inst[5:0]),.op(inst[31:26]),.regdst(regdst),.regw(regw),.alusrc(alusrc),.aluop(aluop),.memw(memw),.memr(memr),.memtoreg(memtoreg),.branch(branch));
RegFile u4(.Rn1(inst[25:21]),.Rn2(inst[20:16]),.Wn(Wn),.Write(regw),.Wd(Wd),.A(A),.B(B),.Clock(Clock));
mux5 u5(.A(inst[20:16]),.B(inst[15:11]),.sel(regdst),.out(Wn));
alu2 u6(.a(A),.b(aluB),.op(aluop),.result(result),.zero(zero));
mux32 u7(.A(B),.B(imm32),.sel(alusrc),.out(aluB));
extnd u8(.data_32bit(imm32),.data_16bit(inst[15:0]));
DATA_RAM u9(.Clock(Clock),.dataout(dataout),.datain(B),.addr(result),.write(memw),.read(memr));
mux32 u10(.A(result),.B(dataout),.sel(memtoreg),.out(Wd));

endmodule
