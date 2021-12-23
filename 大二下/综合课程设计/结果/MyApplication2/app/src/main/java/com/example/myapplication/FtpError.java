package com.example.myapplication;


public class FtpError extends Exception {
	private final String type;

	public FtpError(String a) {
		this.type = a;
	}

	public String getType() {
		return type;
	}
}
