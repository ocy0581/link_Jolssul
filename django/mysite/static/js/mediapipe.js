
var timer = 0;
var count = 3000;
var flag = false;
function send_data(){
    timer = new Date();
    window.setTimeout(()=>{
        chatSocket.send(JSON.stringify({
            'meta' : 'end',
        }))
    },count)
}

const videoElement = document.getElementsByClassName('input_video')[0];
let date = new Date();
var tmp_results;
function onResults(results) {
    // canvasCtx.save();
    // canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);
    // canvasCtx.drawImage(
    //     results.image, 0, 0, canvasElement.width, canvasElement.height);
    // (new Date - date) > 1000 && 
    if((date-timer) < count ){  
        tmp_results = results;
        var json = JSON.stringify({
            'meta' : 'data',
            'landmarks' : results.multiHandLandmarks,
            'handClass' : results.multiHandedness,
        })
        chatSocket.send(json);
        date = new Date()
    }
}

const hands = new Hands({locateFile: (file) => {
    return `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}`;
}});
hands.setOptions({
    maxNumHands: 2,
    minDetectionConfidence: 0.5,
    minTrackingConfidence: 0.5
});
hands.onResults(onResults);

const camera = new Camera(videoElement, {
    onFrame: async () => {
    await hands.send({image: videoElement});
    },
    width: 1280,
    height: 720
});
camera.start();