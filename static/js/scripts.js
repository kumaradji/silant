// static/js/scripts.js

function showTab(tabId) {
    var tabs = document.getElementsByClassName('tab-content');
    for (var i = 0; i < tabs.length; i++) {
        tabs[i].style.display = 'none';
    }
    document.getElementById(tabId).style.display = 'block';
    localStorage.setItem('activeTab', tabId);
}

// Show the default tab
var activeTab = localStorage.getItem('activeTab') || 'machines';
showTab(activeTab);

function showSaveButton(tableId, buttonId) {
    var table = document.getElementById(tableId);
    var button = document.getElementById(buttonId);
    var originalData = [];

    table.querySelectorAll('tbody tr').forEach(row => {
        var rowData = Array.from(row.cells).map(cell => cell.innerText);
        originalData.push(rowData);
    });

    table.addEventListener('input', function() {
        var isChanged = false;
        table.querySelectorAll('tbody tr').forEach((row, rowIndex) => {
            var rowData = Array.from(row.cells).map(cell => cell.innerText);
            if (JSON.stringify(rowData) !== JSON.stringify(originalData[rowIndex])) {
                isChanged = true;
            }
        });
        button.style.display = isChanged ? 'block' : 'none';
    });
}

showSaveButton('machines', 'save-machines-button');
showSaveButton('maintenances', 'save-maintenance-button');
showSaveButton('reclamations', 'save-reclamation-button');

function saveData(url, tableId, buttonId, fields) {
    let rows = document.querySelectorAll(`#${tableId} tbody tr`);
    let data = [];

    rows.forEach(row => {
        let rowData = {
            id: row.getAttribute('data-id')
        };
        fields.forEach((field, index) => {
            rowData[field] = row.cells[index].innerText;
        });
        data.push(rowData);
    });

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        alert('Изменения успешно сохранены!');
        document.getElementById(buttonId).style.display = 'none';
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

document.getElementById('save-machines-button').addEventListener('click', function() {
    saveData('/save_machines/', 'machines', 'save-machines-button', [
        'model_technique', 'serial_number', 'model_engine', 'model_transmission',
        'model_drive_axle', 'model_steering_axle', 'shipment_date'
    ]);
});

document.getElementById('save-maintenance-button').addEventListener('click', function() {
    saveData('/save_maintenances/', 'maintenances', 'save-maintenance-button', [
        'machine', 'maintenance_type', 'maintenance_date', 'operating_time'
    ]);
});

document.getElementById('save-reclamation-button').addEventListener('click', function() {
    saveData('/save_reclamations/', 'reclamations', 'save-reclamation-button', [
        'machine', 'failure_date', 'operating_time', 'failure_unit', 'recovery_method'
    ]);
});

// Добавление обработчика для перехода на детальную информацию только для машин
document.getElementById('machines').addEventListener('click', function(event) {
    if (event.target.tagName === 'TD') {
        var machineId = event.target.parentElement.getAttribute('data-id');
        window.location.href = `/machine/${machineId}/`;
    }
});

// Добавление возможности редактирования ячеек для технического обслуживания и рекламаций
function makeEditable(tableId) {
    var table = document.getElementById(tableId);
    table.querySelectorAll('tbody td.editable').forEach(cell => {
        cell.contentEditable = true;
    });
}

makeEditable('maintenances');
makeEditable('reclamations');