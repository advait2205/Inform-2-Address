function getdetails_onclick(){
    var auth_num=document.getElementById("form_auth_number").value;
    if(auth_num === ""){
        alert("Field cannot be kept empty!");
    }else{
        //document.getElementById("auth_name").innerHTML=authorities[0].name;
        alert(auth_num);
    }
}