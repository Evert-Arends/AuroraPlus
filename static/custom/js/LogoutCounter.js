function startCounter(){
    sec = 5;
    counter = document.getElementById('counter');
    counter.innerText = sec;
    i = setInterval(function(){
        --sec;
        if (sec === 1){
            clearInterval(i);
            window.location = document.getElementById('retry').href;
        }
        counter.innerText=sec;
    },1000);
}

