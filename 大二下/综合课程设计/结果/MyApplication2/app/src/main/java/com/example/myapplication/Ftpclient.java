package com.example.myapplication;

import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.Socket;
import java.util.Vector;

import static java.lang.Character.isWhitespace;

public class Ftpclient {
	private final String host;
	private final String username;
	private final String userpass;
	private final Vector<String> filename = new Vector<>();
	private final Vector<String> dirname = new Vector<>();
	private BufferedReader controlin;
	private PrintWriter controlout;
	private String passhost;
	private int passport;

	public Ftpclient(String host, String name, String pass) {
		username = name;
		userpass = pass;
		this.host = host;
	}

	public void connect() throws IOException {
		Socket socket = new Socket(host, 21);
		controlin = new BufferedReader(new InputStreamReader(socket.getInputStream()));
		controlout = new PrintWriter(new OutputStreamWriter(socket.getOutputStream()), true);
	}

	public void login() throws FtpError, IOException {
		String code;
		//清除开头欢迎信息
		do {
			code = controlin.readLine();
		} while (!code.startsWith("220 "));

		controlout.println("USER " + username);
		code = controlin.readLine();
		if (!code.startsWith("331")) {
			throw new FtpError("用户名错误");
		}

		controlout.println("PASS " + userpass);
		code = controlin.readLine();
		if (!code.startsWith("230")) {
			throw new FtpError("密码错误");
		}
	}

	public void getFileList() throws FtpError, IOException {
		String code;
		String charset = "UTF-8";
		//切换为ascii模式传输
		controlout.println("TYPE A");
		code = controlin.readLine();
		if (!code.startsWith("200")) {
			throw new FtpError("切换为ascii模式失败");
		}
		//使用UTF-8传输
		controlout.println("OPTS UTF8 ON");
		code = controlin.readLine();
		if (!code.startsWith("200")) {
			charset = "GBK";
		}
		pasv();
		dirname.clear();
		filename.clear();
		controlout.println("LIST");
		Socket data = new Socket(passhost, passport);
		code = controlin.readLine();//150 Opening ASCII mode data connection for directory list.
		BufferedReader reader = new BufferedReader(new InputStreamReader(data.getInputStream(), charset));
		//读取文件和文件夹信息
		String a;
		while ((a = reader.readLine()) != null) {
			String b = "";
			int temp = 0, flag = 0;
			for (int i = 0; i < a.length(); i++) {
				if (temp == 7) {
					b = a.substring(i + 1);
				}
				char t = a.charAt(i);
				if (isWhitespace(t)) {
					if (flag == 0) {
						temp++;
						flag = 1;
					}
				} else
					flag = 0;
			}
			if (a.startsWith("d"))
				dirname.add(b);
			else
				filename.add(b);
		}
		reader.close();
		data.close();
		code = controlin.readLine();//XXX Transfer complete
	}

	public String[] getdir() {
		String[] temp = new String[dirname.size()];
		temp = dirname.toArray(temp);
		return temp;
	}

	public String[] getfile() {
		String[] temp = new String[filename.size()];
		temp = filename.toArray(temp);
		return temp;
	}

	public void cdup() throws FtpError, IOException {
		controlout.println("CDUP");
		String code = controlin.readLine();//250 正常 501 失败
		if (!code.startsWith("250"))
			throw new FtpError("无法回到上级目录");
	}

	public void cwd(String name) throws FtpError, IOException {
		controlout.println("CWD " + name);
		String code = controlin.readLine();//250 正常 501 失败
		if (!code.startsWith("250"))
			throw new FtpError("无法回到上级目录");
	}

	private void pasv() throws IOException, FtpError {
		controlout.println("PASV");
		String code = controlin.readLine();
		if (!code.startsWith("227 ")) {
			throw new FtpError("无法使用被动模式");
		}
		int start = code.indexOf('(');
		int end = code.indexOf(')');
		if (end > start) {
			String[] data = code.substring(start + 1, end).split(",");
			if (data.length != 6)
				throw new FtpError("被动模式获取参数错误");
			else {
				passhost = data[0] + "." + data[1] + "." + data[2] + "." + data[3];
				passport = Integer.parseInt(data[4]) * 256 + Integer.parseInt(data[5]);
			}
		}
	}

	public void upload(String name, InputStream is) throws IOException, FtpError {
		String code;
		controlout.println("TYPE I");
		code = controlin.readLine();
		if (!code.startsWith("200")) {
			throw new FtpError("切换为二进制模式失败");
		}
		BufferedInputStream input = new BufferedInputStream(is);
		pasv();
		controlout.println("STOR " + name);
		Socket dataSocket = new Socket(passhost, passport);
		BufferedOutputStream output = new BufferedOutputStream(dataSocket.getOutputStream());
		byte[] buffer = new byte[4096];
		int bytesRead = 0;
		while ((bytesRead = input.read(buffer)) != -1) {
			output.write(buffer, 0, bytesRead);
		}
		output.flush();
		input.close();
		output.close();
		is.close();
		dataSocket.close();
		code = controlin.readLine();
		code = controlin.readLine();
	}

	public void download(String name, OutputStream os) throws IOException, FtpError {
		controlout.println("TYPE I");
		String code = controlin.readLine();
		if (!code.startsWith("200")) {
			throw new FtpError("切换为二进制模式失败");
		}
		pasv();
		controlout.println("RETR " + name);
		Socket dataSocket = new Socket(passhost, passport);
		BufferedOutputStream output = new BufferedOutputStream(os);
		BufferedInputStream input = new BufferedInputStream(dataSocket.getInputStream());
		byte[] buffer = new byte[4096];
		int bytesRead = 0;
		while ((bytesRead = input.read(buffer)) != -1) {
			output.write(buffer, 0, bytesRead);
		}
		output.flush();
		output.close();
		input.close();
		os.close();
		dataSocket.close();
		code = controlin.readLine();
		code = controlin.readLine();
	}

	public void quit() throws IOException, FtpError {
		controlout.println("QUIT");
		String code = controlin.readLine();
		if (!code.startsWith("221")) {
			throw new FtpError("无法退出服务器");
		}
	}

	public void mkd(String path) throws IOException, FtpError {
		controlout.println("MKD /" + path);
		String code = controlin.readLine();
		if (!code.startsWith("257")) {
			throw new FtpError("新建文件夹失败");
		}
	}

	public String pwd() throws IOException, FtpError {
		controlout.println("PWD");
		String code = controlin.readLine();
		if (!code.startsWith("257")) {
			throw new FtpError("获取当前目录失败");
		}
		int start = code.indexOf('"');
		int end = code.indexOf('"', start + 1);
		String path = code.substring(start + 1, end);
		return path;
	}

	public void rnfr(String path) throws IOException, FtpError {
		controlout.println("RNFR " + path);
		String code = controlin.readLine();
		if (!code.startsWith("350")) {
			throw new FtpError("选择要重命名/移动的文件失败");
		}
	}

	public void rnto(String path) throws IOException, FtpError {
		controlout.println("RNTO " + path);
		String code = controlin.readLine();
		if (!code.startsWith("250")) {
			throw new FtpError("重命名/移动失败");
		}
	}

	public void rmd(String path) throws IOException, FtpError {
		controlout.println("RMD " + path);
		String code = controlin.readLine();
		if (!code.startsWith("250")) {
			throw new FtpError("删除文件夹失败，文件夹非空");
		}
	}

	public void dele(String path) throws IOException, FtpError {
		controlout.println("DELE " + path);
		String code = controlin.readLine();
		if (!code.startsWith("250")) {
			throw new FtpError("删除文件失败");
		}
	}

}
