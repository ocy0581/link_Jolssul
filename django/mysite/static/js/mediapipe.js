var timer = 0;
var Mode_Toggle = false
var isRunning = false
var count = 5000;

function send_data(){
    Mode_Toggle = !Mode_Toggle
}

function reset_log(){
    document.getElementById("chat-log").value='';
}

const videoElement = document.getElementsByClassName('input_video')[0];
let date = new Date();
var tmp_results;
var starting_count=0;
var ending_count=0;
function onResults(results) {
    //console.log(isRunning, results.leftHandLandmarks, results.rightHandLandmarks)
    // For Real Time
    console.log(Mode_Toggle)
    if (Mode_Toggle) {
        if (isRunning == false && (results.leftHandLandmarks != undefined ||
            results.rightHandLandmarks != undefined)) {
                isRunning = true
                timer = new Date();
        }

        if((date-timer) < count && isRunning === true){
            // console.log(results)  
            tmp_results = results;
            var json = JSON.stringify({
                'meta': 'data',
                'left': results.leftHandLandmarks,
                'right': results.rightHandLandmarks,
                'pose':results.poseLandmarks,
            })
            //console.log(starting_count, ending_count, isRunning)

            if (ending_count > 20) {
                isRunning = false
                if (starting_count == 21) {
                    webSocket.send(JSON.stringify({
                        'meta' : 'error',
                    }))
                    starting_count = 0
                    ending_count = 0
                    return
                }
                
                webSocket.send(JSON.stringify({
                    'meta' : 'end',
                }))
                starting_count = 0
                ending_count = 0
                return
            }
            if (starting_count > 20 && tmp_results['leftHandLandmarks']== undefined &&
                tmp_results['rightHandLandmarks'] == undefined) {
                ending_count += 1
            } else {
                starting_count += 1
                ending_count = 0
            }
            if (starting_count > 129) {
                isRunning = false
                webSocket.send(JSON.stringify({
                    'meta' : 'error',
                }))
                starting_count = 0
                ending_count = 0
                return
            }
            webSocket.send(json);
            date = new Date()
        }
    }
}                         

// const hands = new Hands({locateFile: (file) => {
//     return `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}`;
// }});
// hands.setOptions({
//     maxNumHands: 2,
//     minDetectionConfidence: 0.5,
//     minTrackingConfidence: 0.5
// });
// hands.onResults(onResults);

// const camera = new Camera(videoElement, {
//     onFrame: async () => {
//     await hands.send({image: videoElement});
//     },

const holistic = new Holistic({locateFile: (file) => {
    return `https://cdn.jsdelivr.net/npm/@mediapipe/holistic/${file}`;
  }});
  holistic.setOptions({
    modelComplexity : 2,
    smoothLandmarks: true,
    minDetectionConfidence: 0.5,
    minTrackingConfidence: 0.5
  });
  holistic.onResults(onResults);
  
  const camera = new Camera(videoElement, {
    onFrame: async () => {
      await holistic.send({image: videoElement});
    },
    width: 1280,
    height: 720
});
camera.start();

