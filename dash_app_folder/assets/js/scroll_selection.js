const checkElement = async selector => {
    while ( document.querySelector(selector) === null) {
        await new Promise( resolve =>  requestAnimationFrame(resolve) )
    }
    return document.querySelector(selector);
};

checkElement('#scroll-div').then((selector) => {
  console.log(selector);
  var obj = document.getElementById('scroll-div');
  obj.scrollTop = obj.scrollHeight;
});