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
      <h2 class="title">${"State: "+ data.state + ", City: " + data.city + ", Region: " + data.region}</h2>
      <img class="post_image" src="${data.image_url}">
      <p class="text">${data.text}</p>
      <p class="date">${"Posted on: " + data.start_time.substring(0,10)}</p>
      <img class="post_upvote" src="https://i.ibb.co/z84z4QD/b9zcqp6w31w51-removebg-preview.jpg" id="post_upv" width="8%" height="8%" >
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

// location modal script

var modal = document.getElementById("locationModal");

// Get the button that opens the modal
var btn = document.getElementById("btn_onClick_location");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks the button, open the modal 
var scnt=0, regcnt=0, citycnt=0, startcnt=0; //onclick counters

function btn_onClick_State(){
  ++scnt;
  regcnt=0;
  citycnt=0;
  startcnt=0;
  modal.style.display = "block";
  document.getElementById("modal_header").innerHTML="Enter the State name which you want to filter";
}

function btn_onClick_Region(){
  ++regcnt;
  scnt=0;
  citycnt=0;
  startcnt=0;
  modal.style.display = "block";
  document.getElementById("modal_header").innerHTML="Enter the Region name which you want to filter"
}

function btn_onClick_City(){
  ++citycnt;
  scnt=0;
  regcnt=0;
  startcnt=0;
  modal.style.display = "block";
  document.getElementById("modal_header").innerHTML="Enter the City name which you want to filter"
}

function btn_onClick_StartTime(){
  ++startcnt;
  scnt=0;
  regcnt=0;
  citycnt=0;
  modal.style.display = "block";
  document.getElementById("modal_header").innerHTML="Enter the Start Time name which you want to filter"
}
function submit_onclick(){
	var filter_val=document.getElementById("loc").value;
    if(filter_val === ""){
    	alert("Field cannot be kept empty!")
    }else{
      if(scnt > 0){
        alert('state');
      }else if(regcnt > 0){
        alert('region');
      }else if(citycnt  > 0){
        alert('city');
      }else if(startcnt > 0){
        alert('start');
      }
      modal.style.display="none";
    }
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}

