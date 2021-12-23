// JavaScript Document
//计算结果变量
var resault = 0;
//前一个按下的运算符
var op = "";
//输入的数字是否从头开始
var isNew = false;
 
$(function () {
    $("#txt").val('0');
    //绑定按钮事件
    //数字输入按钮事件
    $(".number").click(function () {
        if (isNew && this.value != "+/-") {
            $("#txt").val('0');
            isNew = !isNew;
        }
        var currNum = $("#txt").val();
        if (!isNaN(this.value)) //输入的是数字
        {
            if (this.value == 0 && currNum == "0") {
                $("#txt").val('0');
            } else if (this.value != 0 && currNum == "0") {
                $("#txt").val(this.value);
            }
            else {
                $("#txt").val(currNum + this.value);
            }
        } else if (this.value == "+/-")//输入的是负号
        {
            $("#txt").val(0 - parseFloat($("#txt").val()));
        } else if (this.value == "." && currNum.indexOf(".") == -1)//输入的是小数点 并且 当前输入的数字中不包含小数点
        {
            $("#txt").val(currNum + this.value);
        }
    });
 
    //操作符
    $(".op").click(function () {
        getResault();
        op = this.value;
        isNew = true;
    });
 
    //cancel 
    $("#btn_can").click(function () {
        $("#txt").val("0");
        op = "=";
        isNew = false;
        resault = 0;
    });
 
    //clean 
    $("#btn_cle").click(function () {
        $("#txt").val("0");
    });
 
    //del  
    $("#btn_del").click(function () {
        var currStr = $("#txt").val();
        if (currStr.length == 1) {
            $("#txt").val("0");
        } else {
            $("#txt").val(currStr.substr(0, currStr.length - 1));
        }
    });
});
 
//计算结果
function getResault() {
    resault = parseFloat(resault);
    if (op == "+") {
        resault = resault  + parseFloat($("#txt").val()) ;
      } else if (op == "-") {
        resault = resault  - parseFloat($("#txt").val()) ;
      } else if (op == "*") {
        resault = (resault ) * (parseFloat($("#txt").val()) );
      } else if (op == "/") {
        if (parseFloat($("#txt").val()) == 0) {
            resault = 0;
        } else {
            resault = resault / (parseFloat($("#txt").val()) );
        }
    } else {
        resault = $("#txt").val();
    }
    $("#txt").val(resault);
}
