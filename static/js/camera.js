const video = document.getElementById('video');
navigator.mediaDevices.getUserMedia({ video: true })
.then(stream => video.srcObject = stream);

function capture() {
    const canvas = document.getElementById('canvas');
    const image = document.getElementById('image');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext('2d').drawImage(video, 0, 0);
    image.value = canvas.toDataURL('image/png');
}
