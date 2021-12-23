`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    22:14:34 11/13/2015 
// Design Name: 
// Module Name:    Single_Cycle_Computer_IO 
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
module Single_Cycle_Computer_IO(
    input sys_Clock , 		//晶振时钟
	 input BTN_Clock, BTN_Reset,		//按键信号输入
	 
	 output [7:0] seg,		//数码管位码输入
	 output [5:0] AN_SEL,		//数码管段码输入
    output LED0 , LED1		//按键输入指示灯
    );
	 
	 reg  [31:0] clockdiv = 0;		//时钟分频
	 wire  Clock, Reset;		//消抖信号输出
	 wire [31:0] Result, addr;

	 always @ (posedge sys_Clock)  clockdiv <= clockdiv + 1;		//时钟分频
	 BTN_Anti_Jitter Clk ( clockdiv[16] , BTN_Clock , Clock); //按钮去抖动
	 BTN_Anti_Jitter Rst ( clockdiv[16] , BTN_Reset , Reset); //按钮去抖动
	
	 assign LED0 = BTN_Clock;		//按键输入信号
	 assign LED1 = BTN_Reset;		//复位输入信号
 
	 //数码管显示
	 wire [23:0] disp;
	 assign disp = {addr[7:0],Result[31:16]};		//PC低8位+ALU输出高16位
	 Hex7seg_decode hex7(disp , clockdiv[18:16] , seg , AN_SEL);
	 
 	 //************************************************************************************************
	 //端口信号说明：
	 //Reset-复位信号输入；Clock-时钟信号输入；Result-ALU运算结果输出；addr-指令地址
	 //实例化范例：
	 //Single_Cycle_Computer CPU (.Reset(Reset), .Clock(Clock), .Result(Result), .addr(addr));
 	 //************************************************************************************************

	 Single_Cycle_Computer CPU (.Reset(Reset), .Clock(Clock), .Result(Result), .addr(addr));

endmodule
