// for admin login
var form = document.getElementById("loginform");
var submitBtn = document.getElementById("loginBtn");

function adminsubmit() {
    var Email = document.getElementById("Email1").value;
    var password = document.getElementById("password1").value;

    if(Email.indexOf("@")==-1){
        alert("please enter a valid email address!");
        return false;
    }
    else if(password.length!=8){
        alert("password must be 8 characters long!");
        return false;
    }
    else{
        form.submit();
        return true;
    }
}
submitBtn.addEventListener("click", adminsubmit);

// // for admin create
// var form2 = document.getElementById("myForm2");
// var submitBtn2 = document.getElementById("submitBtn2");

// function adminsubmit2() {
//     var Email2 = document.getElementById("Email2").value;
//     var Name2 = document.getElementById("Name2").value;
//     var Mobile2 = document.getElementById("mobile2").value;
//     var password2 = document.getElementById("password2").value;
//     var cpassword2 = document.getElementById("cpassword2").value;
//     let regex2 = /^[a-zA-Z ]+$/;
//     let result2=Name2.match(regex2);
//     regex2 = /^\d+$/;
//     let result22=Mobile2.match(regex2);

//     if(Email2.indexOf("@")==-1){
//         alert("please enter a valid email address!");
//         return false;
//     }
//     else if(!result2){
//         alert("Please enter only alphabets in field Name");
//         return false;
//     }
//     else if(!result22){
//         alert("Please enter only numbers in field Mobile No.");
//         return false;
//     }
//     else if(password2.length!=8){
//         alert("password must be 8 characters long!");
//         return false;
//     }
//     else if(password2!=cpassword2){
//         alert("password and confirm password are not same!");
//         return false;
//     }
//     else{
//         form2.submit();
//         return true;
//     }
// }
// submitBtn2.addEventListener("click", adminsubmit2);

// // for user login-
// var form3 = document.getElementById("myForm3");
// var submitBtn3 = document.getElementById("submitBtn3");

// function adminsubmit3() {
//     var Email3 = document.getElementById("Email3").value;
//     var password3 = document.getElementById("password3").value;

//     if(Email3.indexOf("@")==-1){
//         alert("please enter a valid email address!");
//         return false;
//     }
//     else if(password3.length!=8){
//         alert("password must be 8 characters long!");
//         return false;
//     }
//     else{
//         form3.submit()
//         return true
//     }
// }
// submitBtn3.addEventListener("click", adminsubmit3);

// // for user create
// var form4 = document.getElementById("myForm4");
// var submitBtn4 = document.getElementById("submitBtn4");

// function adminsubmit4() {
//     var Email4 = document.getElementById("Email4").value;
//     var Name4 = document.getElementById("Name4").value;
//     var Mobile4 = document.getElementById("mobile4").value;
//     var password4 = document.getElementById("password4").value;
//     var cpassword4 = document.getElementById("cpassword4").value;
//     let regex4 = /^[a-zA-Z ]+$/;
//     let result4=Name4.match(regex4);
//     regex4 = /^\d+$/;
//     let result24=Mobile4.match(regex4);

//     if(Email4.indexOf("@")==-1){
//         alert("please enter a valid email address!");
//         return false;
//     }
//     else if(!result4){
//         alert("Please enter only alphabets in field Name");
//         return false;
//     }
//     else if(!result24){
//         alert("Please enter only numbers in field Mobile No.");
//         return false;
//     }
//     else if(password4.length!=8){
//         alert("password must be 8 characters long!");
//         return false;
//     }
//     else if(password4!=cpassword4){
//         alert("password and confirm password are not same!");
//         return false;
//     }
//     else{
//         form4.submit();
//         return true;
//     }
// }
// submitBtn4.addEventListener("click", adminsubmit4);
