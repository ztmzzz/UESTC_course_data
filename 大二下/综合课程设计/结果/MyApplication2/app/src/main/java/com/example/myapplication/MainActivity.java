package com.example.myapplication;

import android.content.Intent;
import android.os.Bundle;
import android.os.StrictMode;
import android.view.View;
import android.widget.EditText;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import java.io.IOException;

public class MainActivity extends AppCompatActivity {

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);
		//允许在主线程使用网络
		StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
		StrictMode.setThreadPolicy(policy);
	}

	public void login(View view) {
		Intent intent = new Intent(this, List.class);
		EditText EditText_host = findViewById(R.id.host);
		String host = EditText_host.getText().toString();
		EditText EditText_user = findViewById(R.id.username);
		String user = EditText_user.getText().toString();
		EditText EditText_pass = findViewById(R.id.userpass);
		String pass = EditText_pass.getText().toString();
		Global.ftpclient = new Ftpclient(host, user, pass);
		try {
			Global.ftpclient.connect();
			Global.ftpclient.login();
		} catch (FtpError ftpError) {
			Toast.makeText(getApplicationContext(), ftpError.getType(), Toast.LENGTH_SHORT).show();
		} catch (IOException e) {
			Toast.makeText(getApplicationContext(), "IO错误", Toast.LENGTH_SHORT).show();
			e.printStackTrace();
		}
		startActivity(intent);
	}
}