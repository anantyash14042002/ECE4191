'use strict';

// Global variables
let video = document.querySelector('video');
let videoSelect = document.querySelector('select#videoSource');
let canvas = document.getElementById('canvas');
let context = canvas.getContext('2d');
let frameData = null;
let stream;

// Setup function
function setup() {
  //global variable settings
  videoSelect.onchange = getStream;
  getStream().then(getDevices).then(gotDevices);

  // Set up media constraints
  const constraints = {
    video: true
  };

  // Get user media
  navigator.mediaDevices.getUserMedia(constraints)
    .then(handleSuccess)
    .catch(handleError);
}

// Main loop function
function loop() {
  processVideo();
  requestAnimationFrame(loop);
}

// Helper functions
function handleSuccess(videoStream) {
  stream = videoStream;
  video.srcObject = stream;
  // Start the main loop once we have the stream
  loop();
}

function handleError(error) {
  console.log('getUserMedia error: ', error);
}

function processVideo() {
  // Check if the video is ready and has valid dimensions
  if (video.videoWidth > 0 && video.videoHeight > 0) {
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    
    // Draw the video frame to the canvas
    // Note: This operation can be computationally intensive
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    
    // Get raw pixel data
    frameData = context.getImageData(0, 0, canvas.width, canvas.height);
    console.log(frameData); // Contains raw pixel data
  }
}
function getDevices() {
  return navigator.mediaDevices.enumerateDevices();
}
function gotDevices(deviceInfos) {
  window.deviceInfos = deviceInfos; // make available to console
  console.log('Available input and output devices:', deviceInfos);
  for (const deviceInfo of deviceInfos) {
    if (deviceInfo.kind === 'videoinput') {
      const option = document.createElement('option');
      option.value = deviceInfo.deviceId;
      option.text = deviceInfo.label || `Camera ${videoSelect.length + 1}`;
      videoSelect.appendChild(option);
    }
  }
}
function getStream() {
  if (window.stream) {
    window.stream.getTracks().forEach(track => {
      track.stop();
    });
  }
  const videoSource = videoSelect.value;
  const constraints = {
    video: {deviceId: videoSource ? {exact: videoSource} : undefined}
  };
  return navigator.mediaDevices.getUserMedia(constraints)
    .then(gotStream).catch(handleError);
}

function gotStream(stream) {
  window.stream = stream; // make stream available to console
  videoSelect.selectedIndex = [...videoSelect.options]
    .findIndex(option => option.text === stream.getVideoTracks()[0].label);
  videoElement.srcObject = stream;
}
// Call setup to initialize
setup();