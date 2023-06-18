let departments = document.getElementById('departments');
departments.onclick=()=>{
    if(departments.firstChild.classList.contains("bx-chevron-down")) {
        departments.firstChild.classList.add("bx-chevron-right");
        departments.firstChild.classList.remove("bx-chevron-down");
    } else {
        departments.firstChild.classList.add("bx-chevron-down");
        departments.firstChild.classList.remove("bx-chevron-right");
    }
}