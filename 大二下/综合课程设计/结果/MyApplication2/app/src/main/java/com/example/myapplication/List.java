package com.example.myapplication;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.ContentResolver;
import android.content.DialogInterface;
import android.content.Intent;
import android.database.Cursor;
import android.net.Uri;
import android.os.Bundle;
import android.provider.OpenableColumns;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;
import android.view.View;
import android.widget.AdapterView;
import android.widget.EditText;
import android.widget.ListView;
import android.widget.SimpleAdapter;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

public class List extends AppCompatActivity {
	private final ArrayList<String> all = new ArrayList<>();
	private final ArrayList<Map<String, Object>> listitems = new ArrayList<Map<String, Object>>();
	int[] imageId = new int[]{R.drawable.exe, R.drawable.folder, R.drawable.image, R.drawable.iso, R.drawable.music, R.drawable.other, R.drawable.text, R.drawable.video, R.drawable.zip};
	private String[] dir, file;
	private String downloadName;
	private SimpleAdapter adapter;
	private String selectedpath;

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_list);
		//初始化listview
		getfile();
		adapter = new SimpleAdapter(this, listitems, R.layout.items, new String[]{"filename", "image"}, new int[]{R.id.filename, R.id.image});
		ListView listView = findViewById(R.id.list_view);
		listView.setAdapter(adapter);

		listView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
			@Override
			public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
				if (position < dir.length) {
					if (position == 0) {
						//到当前目录，不需要操作
					} else if (position == 1) {
						//返回上级目录
						try {
							Global.ftpclient.cdup();
						} catch (FtpError ftpError) {
							Toast.makeText(getApplicationContext(), ftpError.getType(), Toast.LENGTH_SHORT).show();
						} catch (IOException e) {
							Toast.makeText(getApplicationContext(), "IO错误", Toast.LENGTH_SHORT).show();
							e.printStackTrace();
						}
						getfile();
						adapter.notifyDataSetChanged();
					} else {
						//进入文件夹
						try {
							Global.ftpclient.cwd(all.get(position));
						} catch (FtpError ftpError) {
							Toast.makeText(getApplicationContext(), ftpError.getType(), Toast.LENGTH_SHORT).show();
						} catch (IOException e) {
							Toast.makeText(getApplicationContext(), "IO错误", Toast.LENGTH_SHORT).show();
							e.printStackTrace();
						}
						getfile();
						adapter.notifyDataSetChanged();
					}
				} else {
					//下载文件
					downloadName = all.get(position);
					downloadDialog();
				}
			}
		});
		listView.setOnItemLongClickListener(new AdapterView.OnItemLongClickListener() {
			@Override
			public boolean onItemLongClick(AdapterView<?> parent, View view, int position, long id) {
				if (position <= 1) {
					//选中当前和上级目录，不需要操作
				} else {
					AlertDialog.Builder builder = new AlertDialog.Builder(listView.getContext());
					builder.setTitle("选择要进行的操作");
					final String[] choice = {"剪切", "重命名", "删除"};
					builder.setItems(choice, new DialogInterface.OnClickListener() {
						@Override
						public void onClick(DialogInterface dialog, int which) {
							String path = null;
							try {
								path = Global.ftpclient.pwd();
							} catch (FtpError ftpError) {
								Toast.makeText(getApplicationContext(), ftpError.getType(), Toast.LENGTH_SHORT).show();
							} catch (IOException e) {
								Toast.makeText(getApplicationContext(), "IO错误", Toast.LENGTH_SHORT).show();
								e.printStackTrace();
							}
							String file = path + "/" + all.get(position);
							switch (which) {
								case 0:
									selectedpath = file;
									break;
								case 1:
									final EditText et = new EditText(listView.getContext());
									String finalPath = path;
									new AlertDialog.Builder(listView.getContext()).setTitle("重命名")
											.setView(et)
											.setPositiveButton("确定", new DialogInterface.OnClickListener() {
												public void onClick(DialogInterface dialog, int which) {
													String input = et.getText().toString();
													if (input.equals("")) {
														Toast.makeText(getApplicationContext(), "新名字不能为空" + input, Toast.LENGTH_LONG).show();
													} else {
														try {
															Global.ftpclient.rnfr(file);
															Global.ftpclient.rnto(finalPath + "/" + input);
															getfile();
															adapter.notifyDataSetChanged();
														} catch (FtpError ftpError) {
															Toast.makeText(getApplicationContext(), ftpError.getType(), Toast.LENGTH_SHORT).show();
														} catch (IOException e) {
															Toast.makeText(getApplicationContext(), "IO错误", Toast.LENGTH_SHORT).show();
															e.printStackTrace();
														}
													}
												}
											})
											.setNegativeButton("取消", null)
											.show();
									break;
								case 2:
									try {
										if (position < dir.length) {
											Global.ftpclient.rmd(file);
										} else {
											Global.ftpclient.dele(file);
										}
										getfile();
										adapter.notifyDataSetChanged();
									} catch (FtpError ftpError) {
										Toast.makeText(getApplicationContext(), ftpError.getType(), Toast.LENGTH_SHORT).show();
									} catch (IOException ee) {
										Toast.makeText(getApplicationContext(), "IO错误", Toast.LENGTH_SHORT).show();
										ee.printStackTrace();
									}
									break;
							}
						}
					});
					builder.show();
				}
				return true;
			}
		});
	}

	public boolean onCreateOptionsMenu(Menu menu) {
		MenuInflater inflater = getMenuInflater();
		inflater.inflate(R.menu.list_menu, menu);
		return true;
	}

	public void upload() {
		Intent intent = new Intent(Intent.ACTION_OPEN_DOCUMENT);
		intent.addCategory(Intent.CATEGORY_OPENABLE);
		intent.setType("*/*");
		startActivityForResult(intent, 2);
	}

	public boolean onOptionsItemSelected(MenuItem item) {
		switch (item.getItemId()) {
			case R.id.uploadfile:
				upload();
				getfile();
				adapter.notifyDataSetChanged();
				return true;
			case R.id.createfolder:
				final EditText et = new EditText(this);
				new AlertDialog.Builder(this).setTitle("请输入要创建的文件夹名字")
						.setView(et)
						.setPositiveButton("确定", new DialogInterface.OnClickListener() {
							public void onClick(DialogInterface dialog, int which) {
								String input = et.getText().toString();
								if (input.equals("")) {
									Toast.makeText(getApplicationContext(), "文件夹名字不能为空" + input, Toast.LENGTH_LONG).show();
								} else {
									try {
										Global.ftpclient.mkd(input);
										getfile();
										adapter.notifyDataSetChanged();
									} catch (FtpError ftpError) {
										Toast.makeText(getApplicationContext(), ftpError.getType(), Toast.LENGTH_SHORT).show();
									} catch (IOException e) {
										Toast.makeText(getApplicationContext(), "IO错误", Toast.LENGTH_SHORT).show();
										e.printStackTrace();
									}
								}
							}
						})
						.setNegativeButton("取消", null)
						.show();
				return true;
			case R.id.paste:
				String nowpath = null;
				try {
					nowpath = Global.ftpclient.pwd();
					Global.ftpclient.rnfr(selectedpath);
					int end = selectedpath.lastIndexOf("/");
					String name = selectedpath.substring(end + 1);
					Global.ftpclient.rnto(nowpath + "/" + name);
					getfile();
					adapter.notifyDataSetChanged();
				} catch (FtpError ftpError) {
					Toast.makeText(getApplicationContext(), ftpError.getType(), Toast.LENGTH_SHORT).show();
				} catch (IOException e) {
					Toast.makeText(getApplicationContext(), "IO错误", Toast.LENGTH_SHORT).show();
					e.printStackTrace();
				}
				selectedpath = null;

			case R.id.refresh:
				getfile();
				adapter.notifyDataSetChanged();
				return true;
			case R.id.exit:
				try {
					Global.ftpclient.quit();
					Intent intent = new Intent(this, MainActivity.class);
					startActivity(intent);
				} catch (FtpError ftpError) {
					Toast.makeText(getApplicationContext(), ftpError.getType(), Toast.LENGTH_SHORT).show();
				} catch (IOException e) {
					Toast.makeText(getApplicationContext(), "IO错误", Toast.LENGTH_SHORT).show();
					e.printStackTrace();
				}
				return true;
			default:
				return super.onOptionsItemSelected(item);
		}
	}

	private void downloadDialog() {
		final AlertDialog.Builder downloadDialog = new AlertDialog.Builder(this);
		downloadDialog.setTitle("下载文件");
		downloadDialog.setMessage("是否要下载?");
		downloadDialog.setPositiveButton("确定",
				new DialogInterface.OnClickListener() {
					@Override
					public void onClick(DialogInterface dialog, int id) {
						//下载文件
						Intent intent = new Intent(Intent.ACTION_CREATE_DOCUMENT);
						intent.addCategory(Intent.CATEGORY_OPENABLE);
						intent.setType("*/*");
						intent.putExtra(Intent.EXTRA_TITLE, downloadName);
						startActivityForResult(intent, 1);
					}
				});
		downloadDialog.setNegativeButton("取消",
				new DialogInterface.OnClickListener() {
					@Override
					public void onClick(DialogInterface dialog, int id) {
					}
				});
		// 显示
		downloadDialog.show();
	}

	@Override
	protected void onActivityResult(int requestCode, int resultCode, Intent data) {
		super.onActivityResult(requestCode, resultCode, data);
		if (data == null) {
			return;
		}
		if (resultCode == Activity.RESULT_OK) {
			Uri uri = data.getData();
			if (requestCode == 1) {
				OutputStream os = null;
				try {
					os = getContentResolver().openOutputStream(uri);
				} catch (FileNotFoundException e) {
					Toast.makeText(getApplicationContext(), "无法找到文件", Toast.LENGTH_SHORT).show();
					e.printStackTrace();
				}
				try {
					Global.ftpclient.download(downloadName, os);
					Toast.makeText(getApplicationContext(), "下载成功", Toast.LENGTH_SHORT).show();
				} catch (FtpError ftpError) {
					Toast.makeText(getApplicationContext(), ftpError.getType(), Toast.LENGTH_SHORT).show();
				} catch (IOException e) {
					Toast.makeText(getApplicationContext(), "IO错误", Toast.LENGTH_SHORT).show();
					e.printStackTrace();
				}
			} else {
				InputStream is = null;
				try {
					is = getContentResolver().openInputStream(uri);
				} catch (FileNotFoundException e) {
					Toast.makeText(getApplicationContext(), "无法找到文件", Toast.LENGTH_SHORT).show();
					e.printStackTrace();
				}

				String uploadName = null;
				ContentResolver contentResolver = this.getContentResolver();
				Cursor cursor = contentResolver.query(uri, null, null, null, null);
				if (cursor.moveToFirst()) {
					uploadName = cursor.getString(cursor.getColumnIndex(OpenableColumns.DISPLAY_NAME));
				}

				try {
					Global.ftpclient.upload(uploadName, is);
					Toast.makeText(getApplicationContext(), "上传成功", Toast.LENGTH_SHORT).show();
				} catch (FtpError ftpError) {
					Toast.makeText(getApplicationContext(), ftpError.getType(), Toast.LENGTH_SHORT).show();
				} catch (IOException e) {
					Toast.makeText(getApplicationContext(), "IO错误", Toast.LENGTH_SHORT).show();
					e.printStackTrace();
				}
				getfile();
				adapter.notifyDataSetChanged();
			}
		}
	}

	private void getfile() {
		try {
			Global.ftpclient.getFileList();
		} catch (FtpError ftpError) {
			Toast.makeText(getApplicationContext(), ftpError.getType(), Toast.LENGTH_SHORT).show();
		} catch (IOException e) {
			Toast.makeText(getApplicationContext(), "IO错误", Toast.LENGTH_SHORT).show();
			e.printStackTrace();
		}
		dir = Global.ftpclient.getdir();
		file = Global.ftpclient.getfile();
		all.clear();
		listitems.clear();
		all.addAll(Arrays.asList(dir));
		all.addAll(Arrays.asList(file));
		for (int i = 0; i < all.size(); i++) {
			Map<String, Object> map = new HashMap<String, Object>();
			int id = 5;
			if (i < dir.length)
				id = 1;
			else {
				String file = all.get(i);
				int end = file.lastIndexOf(".");
				if (end > 0) {
					file = file.substring(end + 1);
					file = file.toLowerCase();
					switch (file) {
						case "exe":
							id = 0;
							break;
						case "jpg":
						case "png":
						case "bmp":
						case "jpeg":
						case "gif":
						case "tif":
							id = 2;
							break;
						case "iso":
							id = 3;
							break;
						case "mp3":
						case "wav":
						case "aac":
						case "flac":
							id = 4;
							break;
						case "txt":
						case "doc":
						case "docx":
							id = 6;
							break;
						case "mp4":
						case "mpeg":
						case "avi":
						case "mov":
						case "flv":
							id = 7;
							break;
						case "zip":
						case "rar":
						case "7z":
						case "gz":
							id = 8;
							break;
					}
				} else
					id = 5;
			}
			map.put("image", imageId[id]);
			map.put("filename", all.get(i));
			listitems.add(map);
		}
	}
}

