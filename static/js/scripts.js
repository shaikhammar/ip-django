/*!
    * Start Bootstrap - SB Admin v7.0.7 (https://startbootstrap.com/template/sb-admin)
    * Copyright 2013-2023 Start Bootstrap
    * Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-sb-admin/blob/master/LICENSE)
    */
    // 
// Scripts
// 

window.addEventListener('DOMContentLoaded', event => {

    // Toggle the side navigation
    const sidebarToggle = document.body.querySelector('#sidebarToggle');
    if (sidebarToggle) {
        // Uncomment Below to persist sidebar toggle between refreshes
        // if (localStorage.getItem('sb|sidebar-toggle') === 'true') {
        //     document.body.classList.toggle('sb-sidenav-toggled');
        // }
        sidebarToggle.addEventListener('click', event => {
            event.preventDefault();
            document.body.classList.toggle('sb-sidenav-toggled');
            localStorage.setItem('sb|sidebar-toggle', document.body.classList.contains('sb-sidenav-toggled'));
        });
    }

});


let addRowButton = document.querySelector('#addRowButton');
let tbody = document.querySelector('#tbody');
let emptyFormRow = document.querySelectorAll('.empty-form');
let totalForms = document.querySelector("#id_invoiceitem_set-TOTAL_FORMS");
let rowCount = document.querySelector('#rowCount');


addRowButton.addEventListener('click', addFormRow)

function addFormRow(e) {
    e.preventDefault();
    let rowCounts = rowCount.value;
    if(rowCounts == ""){ rowCounts = "1"; window.console.error(rowCounts);}
    let formRowNum = totalForms.value;
    while (rowCounts > 0) {
        let newFormRow = emptyFormRow[0].cloneNode(true);
        newFormRow.innerHTML = newFormRow.innerHTML.replaceAll("__prefix__", formRowNum);
        newFormRow.classList = newFormRow.classList.remove();
        tbody.append(newFormRow);
        totalForms.setAttribute('value', parseInt(formRowNum)+1);
        formRowNum = (parseInt(formRowNum) + 1).toString();
        rowCounts = rowCounts - 1;
    }
}

// let deleteRowButton = document.querySelector('.newentry');

// deleteRowButton.addEventListener('click', deleteRow)

// function deleteRow(e) {
//     e.preventDefault();
//     window.console.log(deleteRowButton)
//     var row = e.target.closest('tr');
//     if (row) {
//         row.parentNode.removeChild(row);
//     }
// }

document.addEventListener('DOMContentLoaded', function() {
    document.addEventListener('click', function(event) {
        // Check if the clicked element is an 'a' element with the class 'newentry'
        if (event.target.classList.contains('newentry')) {
            event.preventDefault(); // Prevent the default action of the link
            // Find the closest table row and remove it from the DOM
            var row = event.target.closest('tr');
            if (row) {
                row.parentNode.removeChild(row);
            }
        }
    });
});