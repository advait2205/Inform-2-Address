console.log(complains);

const container = document.querySelector('.container');

let limit = 4;
let pageCount = 1;
let postCount = 0;

const getPost = () => {

    let i = 0;
    for(i = 0; i < limit; i++){
        const htmlData = `
        <div class="posts">
        <p class="post-id">${postCount}</p>    
        <h2 class="title">${complains[postCount].city}</h2>
        <p class="post-info">${complains[postCount].text}</p>
        </div>
        `;
        postCount++;

        container.insertAdjacentHTML('beforeend', htmlData);
    }
};


getPost();

const showData = () => {
    setTimeout(() => {
        pageCount++;
        getPost();
    }, 300)
}

window.addEventListener('scroll', () => {
    // console.log('Hello');
    const {scrollHeight, scrollTop, clientHeight} = document.documentElement;
    // console.log(scrollHeight, scrollTop, clientHeight);
    if(scrollTop + clientHeight > scrollHeight - (1.2 * pageCount)){
        console.log('I am at bottom');
        showData();
    }
});
