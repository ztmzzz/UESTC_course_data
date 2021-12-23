// JavaScript Document
//判断前三个表单元素（用户名、密码、确认密码是否为空）
$(function check( ){
 var check=true;
 var i=0;
for(i=0;i<3;i++){
  if(Form.elements[i].value=="")
  {alert(Form.elements[i].title+"不能为空！");
  Form.elements[i].focus();
  check=false;
  return false;}
  //判断两次输入的密码是否相同
  if(i==2)
  if(Form.pwd.value!=Form.repwd.value)
   {alert("两次输入密码不同，请重新输入！");
  Form.repwd.value="";
     Form.pwd.value="";
  //Form.pwd.focus();
  i=i-2;
  continue;
  }
  
 }
return check;}