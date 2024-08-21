'use strict';
// CLASSES
class SensorData {
  constructor() {
    this.orientation = {
      alpha: 0,
      beta: 0,
      gamma: 0
    };
    this.initialOrientation = {
      alpha: 0,
      beta: 0,
      gamma: 0
    };
    this.accelerometer = {
      x: 0,
      y: 0,
      z: 0
    };
    this.gyroscope = {
      x: 0,
      y: 0,
      z: 0
    };
  }

  setInitialOrientation(alpha, beta, gamma) {
    this.initialOrientation.alpha = alpha;
    this.initialOrientation.beta = beta;
    this.initialOrientation.gamma = gamma;
  }

  updateOrientation(alpha, beta, gamma) {
    this.orientation.alpha = alpha - this.initialOrientation.alpha;
    this.orientation.beta = beta - this.initialOrientation.beta;
    this.orientation.gamma = gamma - this.initialOrientation.gamma;
  }

  updateAccelerometer(x, y, z) {
    this.accelerometer.x = x;
    this.accelerometer.y = y;
    this.accelerometer.z = z;
  }

  updateGyroscope(x, y, z) {
    this.gyroscope.x = x;
    this.gyroscope.y = y;
    this.gyroscope.z = z;
  }

  getAllData() {
    return {
      orientation: this.orientation,
      accelerometer: this.accelerometer,
      gyroscope: this.gyroscope
    };
  }

  getOrientation() {
    return { ...this.orientation };
  }

  getAccelerometer() {
    return { ...this.accelerometer };
  }

  getGyroscope() {
    return { ...this.gyroscope };
  }
}

// Global variables
let video, videoSelect, canvas, context, frameData, videoStream;
let sendDataCheck; // stops client sending same data to server multiple times
const interval = 100; // period of sending data back to the server (ms)
const sensorData = new SensorData();
let motorControl = [1, 1];

// DOM loaded callback
document.addEventListener('DOMContentLoaded', initialiseApp);

function initialiseApp() {
  initialiseElements();
  setupSensors();
  setupMotor();
  setupVideoStream();
}

function initialiseElements() {
  video = document.querySelector('video');
  videoSelect = document.querySelector('select#videoSource');
  canvas = document.getElementById('canvas');
  context = canvas.getContext('2d');
  
  videoSelect.onchange = getVideoStream;
}

// Video processing
function setupVideoStream() {
  getDevices().then(gotDevices).then(getVideoStream);
}

function processVideo() {
  if (video.videoWidth > 0 && video.videoHeight > 0) {
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    frameData = context.getImageData(0, 0, canvas.width, canvas.height);
  }
  requestAnimationFrame(processVideo);
}

// Device handling
async function getDevices() {
  return navigator.mediaDevices.enumerateDevices();
}

function gotDevices(deviceInfos) {
  videoSelect.innerHTML = '';
  for (const deviceInfo of deviceInfos) {
    if (deviceInfo.kind === 'videoinput') {
      const option = document.createElement('option');
      option.value = deviceInfo.deviceId;
      option.text = deviceInfo.label || `Camera ${videoSelect.length + 1}`;
      videoSelect.appendChild(option);
    }
  }
}

async function getVideoStream() {
  if (videoStream) {
    videoStream.getTracks().forEach(track => track.stop());
  }
  const videoSource = videoSelect.value;
  const constraints = {
    video: { deviceId: videoSource ? { exact: videoSource } : undefined }
  };
  try {
    videoStream = await navigator.mediaDevices.getUserMedia(constraints);
    gotVideoStream(videoStream);
  } catch (error) {
    console.error('Error accessing media devices.', error);
  }
}

function gotVideoStream(newVideoStream) {
  videoStream = newVideoStream;
  video.srcObject = videoStream;
  requestAnimationFrame(processVideo);
  const activeTrack = videoStream.getVideoTracks()[0];
  videoSelect.value = activeTrack.getSettings().deviceId;
}

// Sensor handling
function setupSensors() {
  const enableSensorsBtn = document.getElementById('enableSensors');
  if (typeof DeviceMotionEvent.requestPermission === 'function') {
    enableSensorsBtn.style.display = 'block';
    enableSensorsBtn.addEventListener('click', requestIOSPermission);
  } else {
    initialiseSensors();
  }
}

async function requestIOSPermission() {
  try {
    const response = await DeviceMotionEvent.requestPermission();
    if (response === "granted") {
      initialiseSensors();
    }
  } catch (error) {
    console.error("Error requesting iOS permission", error);
  }
}

function initialiseSensors() {
  try {
    window.addEventListener("devicemotion", handleMotion);
    window.addEventListener("deviceorientation", handleOrientation);
  } catch (error) {
    console.error("Sensor APIs not supported", error);
  }
}
//motor button
function setupMotor() {
  const motorBtn = document.getElementById('enableMotors');
  motorBtn.addEventListener('click', motorOffOn);
}
function motorOffOn(){
  motorControl[0] = 1 - motorControl[0];
  motorControl[1] = 1 - motorControl[1];
  console.log(motorControl);
}
function handleOrientation(event) {
  // Update the orientation data correctly
  sensorData.updateOrientation(event.alpha, event.beta, event.gamma);
  
  // Also update the display fields
  updateFieldIfNotNull('Orientation_a', event.alpha);
  updateFieldIfNotNull('Orientation_b', event.beta);
  updateFieldIfNotNull('Orientation_g', event.gamma);
}

function handleMotion(event) {
  const { acceleration, rotationRate } = event;
  sensorData.updateAccelerometer(acceleration.x, acceleration.y, acceleration.z);
  sensorData.updateGyroscope(rotationRate.alpha, rotationRate.beta, rotationRate.gamma);
  
  updateFieldIfNotNull('Accelerometer_x', acceleration.x);
  updateFieldIfNotNull('Accelerometer_y', acceleration.y);
  updateFieldIfNotNull('Accelerometer_z', acceleration.z);
  
  updateFieldIfNotNull('Gyroscope_x', rotationRate.alpha);
  updateFieldIfNotNull('Gyroscope_y', rotationRate.beta);
  updateFieldIfNotNull('Gyroscope_z', rotationRate.gamma);
}

function updateFieldIfNotNull(fieldName, value, precision = 3) {
  if (value != null) {
    document.getElementById(fieldName).innerHTML = value.toFixed(precision);
  }
}


// Sending data back to the server
function sendDataToServer(data) {
  fetch('/api/clientData', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data)
  })
  .then(response => response.json())
  .then(result => {
    console.log('Data sent successfully:', result);
  })
  .catch(error => {
    console.error('Error sending data:', error);
  });
}

// New function to start periodic data sending
function startPeriodicDataSending() {
  if (sendDataCheck) {
    clearInterval(sendDataCheck);
  }
  sendDataCheck = setInterval(() => {
    const sensorDataPayload = sensorData.getAllData();
    const data = {
      sensorData: sensorDataPayload,
      motorControlData: motorControl
    };
    sendDataToServer(data);
  }, interval);
}

// Start sending data immediately after initialization
document.addEventListener('DOMContentLoaded', () => {
  initialiseApp();
  startPeriodicDataSending();
});
