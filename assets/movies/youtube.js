
let tag = document.createElement('script');
tag.src = "https://www.youtube.com/iframe_api";
let firstScriptTag = document.getElementsByTagName('script')[0]
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag)
const APIKEY = 'AIzaSyDPnDtMx0BMQUBJ9XwpImGCHF_a53saP7s'

let player
let video
var done = false;

axios.get(`https://www.googleapis.com/youtube/v3/search`, {
    params: {
        key: APIKEY,
        part: 'id',
        q: title.value + '예고편',
        maxResults: 1,
    }})
    .then(response => {
        console.log(response.data.items)
        video = response.data.items[0].id.videoId
        })

function onYouTubeIframeAPIReady() {
    player = new YT.Player('ytp', {
        height: '400px',
        width: '100%',
        videoId: video,
        events: {
            'onReady': onPlayerReady,
            'onStateChange': onPlayerStateChange
        }
    });
}

function onPlayerReady(event) {
    event.target.playVideo();
}


function onPlayerStateChange(event) {
    if (event.data == YT.PlayerState.PLAYING && !done) {
        setTimeout(stopVideo, 10000)
        done = true
    }
}

function stopVideo() {
    player.stopVideo()
}