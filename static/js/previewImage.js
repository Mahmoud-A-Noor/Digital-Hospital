function previewImage(event, img_container) {
    const reader = new FileReader();
    reader.onload = function() {
        const element = img_container;
        element.src = reader.result;
    }
    reader.readAsDataURL(event.target.files[0]);
}

const input1 = document.querySelector('#img');

const img_container1 = document.querySelector('#previewImage');
input1.addEventListener('change', (event) => {
    previewImage(event, img_container1);
    img_container1.classList.remove('d-none');
});