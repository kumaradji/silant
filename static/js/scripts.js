function showTab(tabId) {
    var tabs = document.getElementsByClassName('tab-content');
    for (var i = 0; i < tabs.length; i++) {
        tabs[i].style.display = 'none';
    }
    document.getElementById(tabId).style.display = 'block';
    localStorage.setItem('activeTab', tabId);
}

var activeTab = localStorage.getItem('activeTab') || 'machines';
showTab(activeTab);

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

document.getElementById('save-maintenance-button').addEventListener('click', function() {
    let rows = document.querySelectorAll('#maintenances tbody tr');
    let data = [];

    rows.forEach(row => {
        let rowData = {
            id: row.getAttribute('data-id'),
            maintenance_type: row.cells[1].innerText.trim(),
            maintenance_date: row.cells[2].innerText.trim(),
            operating_time: row.cells[3].innerText.trim()
        };
        data.push(rowData);
    });

    console.log('Data to be sent:', JSON.stringify(data, null, 2));

    fetch('/save_maintenances/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            alert('Изменения успешно сохранены!');
            document.getElementById('save-maintenance-button').style.display = 'none';
        } else {
            alert(`Произошла ошибка при сохранении изменений: ${data.message}`);
        }
    })
    .catch((error) => {
        console.error('Error:', error);
        alert('Произошла ошибка при сохранении изменений');
    });
});

document.getElementById('save-reclamation-button').addEventListener('click', function() {
    let rows = document.querySelectorAll('#reclamations tbody tr');
    let data = [];

    rows.forEach(row => {
        let rowData = {
            id: row.getAttribute('data-id'),
            failure_date: row.cells[1].innerText.trim(),
            operating_time: row.cells[2].innerText.trim(),
            failure_unit: row.cells[3].innerText.trim(),
            recovery_method: row.cells[4].innerText.trim()
        };
        data.push(rowData);
    });

    console.log('Data to be sent:', JSON.stringify(data, null, 2));

    fetch('/save_reclamations/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            alert('Изменения успешно сохранены!');
            document.getElementById('save-reclamation-button').style.display = 'none';
        } else {
            alert(`Произошла ошибка при сохранении изменений: ${data.message}`);
        }
    })
    .catch((error) => {
        console.error('Error:', error);
        alert('Произошла ошибка при сохранении изменений');
    });
});

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

function makeEditable(tableId) {
    var table = document.getElementById(tableId);
    table.querySelectorAll('tbody td.editable').forEach(cell => {
        cell.contentEditable = true;
    });
}

makeEditable('maintenances');
makeEditable('reclamations');
