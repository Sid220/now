"use strict";

function timerPauseAnim() {
    [...document.getElementsByClassName('loading-hold')].forEach((ele) => {
        ele.getElementsByClassName('loading-fill')[0].style.animationPlayState = "paused";
    });
}

function timerPlayAnim() {
    [...document.getElementsByClassName('loading-hold')].forEach((ele) => {
        let el = ele.getElementsByClassName('loading-fill')[0];
        el.style.animation = 'none';
        el.offsetHeight; /* trigger reflow */
        el.style.animation = null;
        el.style.animationPlayState = "running";
    });
}


let vid_ids = [];
let iframe = document.getElementById('player-iframe');
let timer = document.getElementById('player-timer');
let pause = document.getElementById('player-pause');

let currentTime = 0;
let updateTimeInterval;
let paused = false;
const maxTime = 15;

function updateTime() {
    if (!paused) {
        currentTime++;
    }
    if (currentTime === maxTime) {
        console.log("Time up");
        newVideo();
    }
}

function resetTime() {
    clearInterval(updateTimeInterval);
    currentTime = 0;
}

function newVideo() {
    function postLoad() {
        resetTime();
        updateTime();
        updateTimeInterval = setInterval(updateTime, 1000);
        timerPlayAnim();
    }

    timerPauseAnim();
    vid_ids.shift();
    if (vid_ids.length === 0) {
        $.ajax({
            dataType: 'json',
            url: '/api/get_vids',
            success: function (data) {
                vid_ids = data;
                console.log("Success retrieving videos");
                iframe.src = "https://www.youtube.com/embed/" + vid_ids[0] + "?autoplay=1&enablejsapi=1&playsinline=1";
                postLoad();
            },
            error: function () {
                console.error("Error retrieving videos");
            }
        });
    } else {
        iframe.src = "https://www.youtube.com/embed/" + vid_ids[0] + "?autoplay=1&enablejsapi=1&playsinline=1";
        postLoad();
    }
}

// newVideo();

timer.addEventListener('click', function () {
    newVideo();
});

pause.addEventListener('click', function () {
    paused = !paused;
    let pauseMainEle = pause.getElementsByClassName("control-main")[0];
    if (paused) {
        currentTime = 0;
        pauseMainEle.innerHTML = '<i class="bi bi-stopwatch"></i>';
        timerPauseAnim();
    } else {
        pauseMainEle.innerHTML = '<i class="bi bi-stopwatch-fill"></i>';
        timerPlayAnim();
    }
});

$.ajax({
    dataType: 'json',
    url: 'https://epic.gsfc.nasa.gov/api/natural',
    success: function (data) {
        console.log("Success retrieving images");
        document.body.style.backgroundImage = "url(\"https://epic.gsfc.nasa.gov/archive/natural/" + data[0].date.split(" ")[0].replace(/-/g, "/") + "/png/" + data[0].image + ".png\")";
    },
    error: function () {
        console.error("Error retrieving images");
    }
})

document.getElementById("begin-button").addEventListener("click", function () {
    newVideo();
    document.getElementById("cover").style.display = "none";
    iframe.style.display = "block";
    timer.style.display = "flex";
    pause.style.display = "block";
});
