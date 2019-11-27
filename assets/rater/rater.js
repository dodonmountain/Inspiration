const star1 = document.getElementById('star1')
const star2 = document.getElementById('star2')
const star3 = document.getElementById('star3')
const star4 = document.getElementById('star4')
const star5 = document.getElementById('star5')
const star6 = document.getElementById('star6')
const star7 = document.getElementById('star7')
const star8 = document.getElementById('star8')
const star9 = document.getElementById('star9')
const star10 = document.getElementById('star10')
let sendList = [];
let isStopped = false;
const Stars = [star1, star2, star3, star4, star5, star6, star7, star8, star9, star10]
let pressedScore;
pressedScore = 0
let passThis = false;
let movieNow = 1;
let target = document.querySelectorAll('.carousel-tile')[movieNow]
let colors = ['royalblue', 'orange', 'darkviolet', 'hotpink', 'tomato', 'crimson', 'seagreen']
let random_color = colors[Math.floor(Math.random() * colors.length)];

function sideScroll(direction, speed, distance, step) {
    scrollAmount = 0;
    var slideTimer = setInterval(function() {
        if (direction == 'left') {
            car.scrollLeft -= step;
        } else {
            car.scrollLeft += step;
        }
        scrollAmount += step;
        if (scrollAmount >= distance) {
            window.clearInterval(slideTimer);
        }
    }, speed);
}
const rLeft = document.getElementById('rateLeft')
let former;
window.onkeydown = function() {
    if (!isStopped) {
        document.querySelector('.RaterDescription').hidden = true
        pressedScore = 0
        if (event.key == '1') {
            pressedScore = 1
        } else if (event.key == '2') {
            pressedScore = 2
        } else if (event.key == '3') {
            pressedScore = 3
        } else if (event.key == '4') {
            pressedScore = 4
        } else if (event.key == '5') {
            pressedScore = 5
        } else if (event.key == '6') {
            pressedScore = 6
        } else if (event.key == '7') {
            pressedScore = 7
        } else if (event.key == '8') {
            pressedScore = 8
        } else if (event.key == '9') {
            pressedScore = 9
        } else if (event.key == '0') {
            pressedScore = 10
        } else if (event.keyCode == 32) {
            passThis = true
        }
        if (0 < pressedScore && pressedScore < 11) {
            for (let i = 0; i < pressedScore; i++) {
                setTimeout(() => {
                    Stars[i].classList.add('twinkle')
                }, 250)
                Stars[i].classList.remove('twinkle')
            };
            car.scrollLeft += 629.2
            target = document.querySelectorAll('.carousel-tile')[movieNow]
            target.classList.remove('carousel-tile-hover')
            let movie_id = target.firstElementChild.innerText
            document.getElementById('starForm').firstElementChild.value += '/'+ String(pressedScore) + '/' + movie_id
            sendList.push([parseInt(movie_id),pressedScore])
            movieNow += 1
            document.querySelectorAll('.carousel-tile')[movieNow].classList.add('carousel-tile-hover')
            if (parseInt(rLeft.innerText) <= 1) {
                document.querySelector('.scoreForNow').innerText = 'THANK YOU'
                let thx = document.querySelector('.scoreForNow').innerText = 'THANK YOU'
                former.parentNode.append(thx)
                isStopped = true
                car.hidden = true
                document.getElementById('starSubmit').click()
            }
            rLeft.innerText -= 1
            former = document.querySelector('.scoreForNow')
            random_color = colors[Math.floor(Math.random() * colors.length)];
            document.querySelector('.scoreForNow').style.color = random_color
            former.innerText = pressedScore
            let cln = former.cloneNode(true)
            former.parentNode.appendChild(cln)
            former.classList.add('scoreFormer')
            widthNow = 100
            clearInterval()
            setTimeout(() => {
                former.hidden = true
                former.classList.remove('scoreForNow')
            }, 300);
        };
    }






}
const timer = document.getElementById('timer')
let widthNow;
setInterval(() => {
    timer.style.width = widthNow + "%"
    if (widthNow < 0) {
        stopAll()
        document.querySelector('.scoreForNow').innerText = 'TRY AGAIN'
    }
}, 1000);
setInterval(() => {
    widthNow -= 1
}, 150);

function stopAll() {
    isStopped = true
    timer.hidden = true
    timer.parentElement.hidden = true
}