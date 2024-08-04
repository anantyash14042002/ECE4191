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
  // Set up event listener for camera selection
  videoSelect.onchange = getStream;

  // Get initial list of devices
  getDevices().then(gotDevices).then(getStream);
}

// Main loop function
function loop() {
  processVideo();
  requestAnimationFrame(loop);
}

function processVideo() {
  // Check if the video is ready and has valid dimensions
  if (video.videoWidth > 0 && video.videoHeight > 0) {
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    
    // Draw the video frame to the canvas
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
  videoSelect.innerHTML = ''; // Clear existing options
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
  if (stream) {
    stream.getTracks().forEach(track => track.stop());
  }
  const videoSource = videoSelect.value;
  const constraints = {
    video: {deviceId: videoSource ? {exact: videoSource} : undefined}
  };
  return navigator.mediaDevices.getUserMedia(constraints)
    .then(gotStream)
    .catch(handleError);
}

function gotStream(videoStream) {
  stream = videoStream;
  video.srcObject = stream;
  // Start the main loop once we have the stream
  requestAnimationFrame(loop);
  
  // Update the select element to show the currently active device
  const activeTrack = stream.getVideoTracks()[0];
  videoSelect.value = activeTrack.getSettings().deviceId;
}

function handleError(error) {
  console.error('Error: ', error);
}

// Call setup to initialize
setup();