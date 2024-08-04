'use strict';

// Global variables
let video;
let canvas;
let context;
let frameData;
let stream;

// Setup function
function setup() {
  video = document.querySelector('video');
  canvas = document.getElementById('canvas');
  context = canvas.getContext('2d');
  frameData = null;

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

// Call setup to initialize
setup();