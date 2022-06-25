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
      <h2 class="title">${data.city}</h2>
      <img class="post_image" src="${data.image_url}">
      <p class="text">${data.text}</p>
      <img class="post_upvote" src="https://i.ibb.co/z84z4QD/b9zcqp6w31w51-removebg-preview.jpg" id="post_upv" width="8%" height="8%" onclick="changeImage()">
    `;
    container.appendChild(postElement);
  
    loading.classList.remove('show');
  }

function myFunction() {
    document.getElementById("myDropdown").classList.toggle("show");
}

function btn_click1(){
	var x=document.getElementById("fuckoff")
    x.innerHTML="aaah"
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