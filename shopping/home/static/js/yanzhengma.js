function showCheck(a){
    var c = document.getElementById("myCanvas");
    var ctx = c.getContext("2d");
    ctx.clearRect(0,0,1000,1000);
    ctx.font = "80px 'Microsoft Yahei'";
    ctx.fillText(a,0,100);
    ctx.fillStyle = "white";
}
var code ;
function createCode(){
    code = "";
    var codeLength = 4;
    var selectChar = new Array(1,2,3,4,5,6,7,8,9,'a','b','c','d','e','f','g','h','j','k','l','m','n','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','J','K','L','M','N','P','Q','R','S','T','U','V','W','X','Y','Z');
    for(var i=0;i<codeLength;i++) {
       var charIndex = Math.floor(Math.random()*60);
      code +=selectChar[charIndex];
    }
    if(code.length != codeLength){
        //递归函数，刷新验证码
      createCode();
    }
    showCheck(code);
}

function validate () {
    var inputCode = document.getElementById("J_codetext").value.toUpperCase();
    var codeToUp=code.toUpperCase();
    if(inputCode.length <=0) {
      document.getElementById("J_codetext").setAttribute("placeholder","输入验证码");
      createCode();
      return false;
    }
    else if(inputCode != codeToUp ){
      document.getElementById("J_codetext").value="";
      document.getElementById("J_codetext").setAttribute("placeholder","验证码错误");
      createCode();
      return false;
    }
    else {
       //验证正确打开新的窗口
      //window.open(document.getElementById("J_down").getAttribute("data-link"));
      //window.open("index");
      // 把输入的验证码重置为空
      document.getElementById("J_codetext").value="";
      createCode();
         //serialize() 方法通过序列化表单值，创建 URL 编码文本字符串。
        $.ajax({
            type:"POST",
            dataType:"json",
            url:"is_login",
            data:$('#form1').serialize(),
            success:function (data) {
                if(data.sex=="nan"){
                    alert("登录成功！");
                    location.href="index"
                }else{
                    // 用一个标签来提示用户账号密码错误，使网页更友善
                    alert("账号或密码错误！");
                    location.href="login"
                }
            },
            error:function(){
                alert("异常");
            }
        });
      return true;
    }

}