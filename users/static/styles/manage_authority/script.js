// location modal script

var modal = document.getElementById("locationModal");

// Get the button that opens the modal
var btn = document.getElementById("btn_onClick_location");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

var aacnt=0, rcnt=0;

function add_auth_onclick(){
    ++aacnt;
    rcnt=0;
    var auth_mob_num=document.getElementById("form_mob_num").value; // gets mob num of auth added in form on main page
    if(auth_mob_num === ""){
        alert("Empty Field Not allowed");
    }else{
      //  alert(auth_mob_num);
        modal.style.display="block";
        document.getElementById("modal_h2").innerHTML="Enter Category Name"
        document.getElementById("modal_header").innerHTML="Enter the category name in which you want to add " + auth_mob_num;
    }
}

function remove_auth_onclick(){
    ++rcnt;
    aacnt=0;
    var cate=document.getElementById("form_get_cat").value;
    if(cate === ""){
        alert("Empty Field Not Allowed");
    }else{
        modal.style.display="block";
        document.getElementById("modal_h2").innerHTML="Enter Mobile Number"
        document.getElementById("modal_header").innerHTML="Enter the mobile number of authority you want to remove from category "+ cate;
    }
}

function submit_onclick(){
    var inputt=document.getElementById("modal_input").value;
    if(inputt === ""){
        alert("Empty Field Not allowed")
    }
    else{
        if(aacnt > 0){
            alert("The category name is " + inputt);
        }else if(rcnt > 0){
            alert("The mobile number is " + inputt);
        }
        modal.style.display="none";
    }
}

span.onclick = function() {
    modal.style.display = "none";
}
  
// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
      modal.style.display = "none";
    }
}