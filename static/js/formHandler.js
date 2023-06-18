let gender = document.getElementById('gender');
let pregnant = document.getElementById('pregnant');

gender.onchange=()=>{
    if (gender.value == "0") {
        pregnant.classList.remove('d-none');
        pregnant.classList.remove('d-block');
    } else {
        pregnant.classList.remove('d-block');
        pregnant.classList.add('d-none');
    }
}

function removeInput(inputName) {
    let input_div = document.getElementById(`${inputName}`);
    let input = document.querySelector(`input[name='${inputName}']`);
    input.value = 0;
    input_div.classList.add('d-none');
    input_div.classList.remove('d-block');
}

function displayInput(inputName) {
    let input_div = document.getElementById(`${inputName}`);
    let input = document.querySelector(`input[name='${inputName}']`);
    input.value = null;
    input_div.classList.remove('d-none');
    input_div.classList.add('d-block');
}