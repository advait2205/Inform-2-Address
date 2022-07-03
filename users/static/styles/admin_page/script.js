function getdetails_onclick(){
    var auth_num=document.getElementById("form_auth_number").value;
    if(auth_num === ""){
        alert("Field cannot be kept empty!");
    }else{
        //document.getElementById("auth_name").innerHTML=authorities[0].name;
        alert(auth_num);
    }
}

console.log(complains);
  
const container = document.getElementById('container');
const loading = document.querySelector('.loading');
let post_offset = 0;

//   getPost();
//   getPost();
//   getPost();

  for (let index = 0; index < 5; index++) {
      getPost();
  }

window.addEventListener('scroll', () => {
  const { scrollTop, scrollHeight, clientHeight } = document.documentElement;

  if(clientHeight + scrollTop >= scrollHeight - 5) {
    // show the loading animation
    showLoading();
  }
});

function showLoading() {
  if(post_offset < complains.length){
    loading.classList.add('show');

    // load more data
    setTimeout(getPost, 300)
  }
  else{
    // end has been reached, no more posts available
  }
}

async function getPost() {
  console.log(post_offset)
  if(post_offset < complains.length){
    addDataToDOM(complains[post_offset]);
    post_offset++;
  }
}
// https://i.ibb.co/SPjZ97Y/imgonline-com-ua-Replace-Color-s-Z9-Bt-Ug911i-A.jpg  -- green image
function addDataToDOM(data) {
  const postElement = document.createElement('div');
  postElement.classList.add('blog-post');
  postElement.innerHTML = `
    <img class="post_image" src="${data.image_url}">
    <p class="text">${data.text}</p>
    <h4 class="date">${data.region + ", " + data.city + ", " + data.state}</h4>
    <p class="date">${"Posted on: " + data.start_time.substring(0,10)}
    &nbsp; &nbsp;&nbsp;&nbsp;&nbsp;${"Expected Resolve Date: " + data.end_time.substring(0,10)}
    &nbsp; &nbsp;&nbsp;&nbsp;&nbsp;${"Upvotes: " + data.upvotes}</p>
  `;
  container.appendChild(postElement);

  loading.classList.remove('show');
}

//document.getElementById("post_upv").addEventListener("click", changeImage());

function myFunction() {
  document.getElementById("myDropdown").classList.toggle("show");
}


window.onclick = function(e) {
  if (!e.target.matches('.dropbtn')) {
  var myDropdown = document.getElementById("myDropdown");
    if (myDropdown.classList.contains('show')) {
      myDropdown.classList.remove('show');
    }
  }
}

//   function changeImage(){
//     if(document.getElementById("post_upv").src == "https://i.ibb.co/z84z4QD/b9zcqp6w31w51-removebg-preview.jpg"){
//         document.getElementById("post_upv").src= "https://i.ibb.co/SPjZ97Y/imgonline-com-ua-Replace-Color-s-Z9-Bt-Ug911i-A.jpg"
//     }
// }