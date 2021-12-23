`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    22:34:22 11/13/2015 
// Design Name: 
// Module Name:    BTN_Anti_Jitter 
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
module BTN_Anti_Jitter(
		input Clock,
		input BTN_IN,
		output reg BTN_Out
    );
	 
	 reg [3:0] cnt;
	 
	 always @ (posedge Clock)
		if(cnt == 4'b1111)
			begin
				cnt <= 4'b0000; BTN_Out <= BTN_IN;
			end
		else
			cnt <= cnt + 1'b1;
			
endmodule

