/*!
 * Start Bootstrap - SB Admin v7.0.7 (https://startbootstrap.com/template/sb-admin)
 * Copyright 2013-2023 Start Bootstrap
 * Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-sb-admin/blob/master/LICENSE)
 */
//
// Scripts
//

window.addEventListener("DOMContentLoaded", (event) => {
  // Toggle the side navigation
  const sidebarToggle = document.body.querySelector("#sidebarToggle");
  if (sidebarToggle) {
    // Uncomment Below to persist sidebar toggle between refreshes
    // if (localStorage.getItem('sb|sidebar-toggle') === 'true') {
    //     document.body.classList.toggle('sb-sidenav-toggled');
    // }
    sidebarToggle.addEventListener("click", (event) => {
      event.preventDefault();
      document.body.classList.toggle("sb-sidenav-toggled");
      localStorage.setItem(
        "sb|sidebar-toggle",
        document.body.classList.contains("sb-sidenav-toggled")
      );
    });
  }
});

let addRowButton = document.querySelector("#addRowButton");
let tbody = document.querySelector("#tbody");
let emptyFormRow = document.querySelectorAll(".empty-form");
let totalForms = document.querySelector("#id_invoiceitem_set-TOTAL_FORMS");
let rowCount = document.querySelector("#rowCount");

addRowButton.addEventListener("click", addFormRow);

function addFormRow(e) {
  e.preventDefault();
  let rowCounts = rowCount.value;
  if (rowCounts == "") {
    rowCounts = "1";
    window.console.error(rowCounts);
  }
  let formRowNum = totalForms.value;
  while (rowCounts > 0) {
    let newFormRow = emptyFormRow[0].cloneNode(true);
    newFormRow.innerHTML = newFormRow.innerHTML.replaceAll(
      "__prefix__",
      formRowNum
    );
    newFormRow.classList = newFormRow.classList.remove();
    tbody.append(newFormRow);
    totalForms.setAttribute("value", parseInt(formRowNum) + 1);
    formRowNum = (parseInt(formRowNum) + 1).toString();
    rowCounts = rowCounts - 1;
  }
}

document.addEventListener("DOMContentLoaded", function () {
  document.addEventListener("click", function (event) {
    // Check if the clicked element is an 'a' element with the class 'newentry'
    if (event.target.classList.contains("newentry")) {
      event.preventDefault(); // Prevent the default action of the link
      // Find the closest table row and remove it from the DOM
      var row = event.target.closest("tr");
      if (row) {
        row.parentNode.removeChild(row);
      }
    }
  });
});

document.addEventListener('DOMContentLoaded', function() {
    const tbody = document.getElementById('tbody');
    const invoiceTotalInput = document.getElementById('id_invoice_total');

    function updateTotals() {
      let total = 0;
      const rows = tbody.querySelectorAll('tr');
      rows.forEach(row => {
        const deleteCheckbox = row.querySelector('[id^="id_invoiceitem_set-"][id$="-DELETE"]');
        if (!deleteCheckbox || !deleteCheckbox.checked) {
          const itemTotal = parseFloat(row.querySelector('[id^="id_invoiceitem_set-"][id$="-item_total"]').value) || 0;
          total += itemTotal;
        }
      });
      if(total != 0){
        document.getElementById('id_invoice_total').value = total.toFixed(2);
      }
    }

    function updateItemTotal(row) {
      const quantity = parseFloat(row.querySelector('[id^="id_invoiceitem_set-"][id$="-item_quantity"]').value) || 0;
      const price = parseFloat(row.querySelector('[id^="id_invoiceitem_set-"][id$="-item_price"]').value) || 0;
      const total = quantity * price;
      if(total != 0){
        row.querySelector('[id^="id_invoiceitem_set-"][id$="-item_total"]').value = total.toFixed(2);
      }
    }

    function observeChanges() {
      const observer = new MutationObserver(mutations => {
        mutations.forEach(mutation => {
          if (mutation.type === 'childList') {
            updateTotals();
          }
        });
      });

      const config = { childList: true, subtree: true };
      observer.observe(tbody, config);
    }

    function setupListeners() {
      tbody.addEventListener('keyup', function(event) {
        if (event.target.matches('[id^="id_invoiceitem_set-"][id$="-item_quantity"]') || event.target.matches('[id^="id_invoiceitem_set-"][id$="-item_price"]')) {
          const row = event.target.closest('tr');
          updateItemTotal(row);
          updateTotals();
        }
      });

      tbody.addEventListener('change', function(event) {
        if (event.target.matches('[id^="id_invoiceitem_set-"][id$="-DELETE"]')) {
          updateTotals();
        }
      });
    }

    observeChanges();
    setupListeners();
  });

// document.querySelectorAll('.numberinput').forEach(function(input) {
//     input.addEventListener('change', updateTotals());
// });
