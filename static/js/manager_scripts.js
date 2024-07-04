document.addEventListener("DOMContentLoaded", function() {
    function showTab(tabId) {
        var tabs = document.getElementsByClassName('tab-content');
        for (var i = 0; i < tabs.length; i++) {
            tabs[i].style.display = 'none';
        }
        document.getElementById(tabId).style.display = 'block';
        localStorage.setItem('activeTab', tabId);

        var tabButtons = document.getElementsByClassName('tab');
        for (var i = 0; i < tabButtons.length; i++) {
            tabButtons[i].classList.remove('active');
        }

        var activeButton = document.querySelector(`.tab[onclick="showTab('${tabId}')"]`);
        if (activeButton) {
            activeButton.classList.add('active');
        }
    }

    var activeTab = localStorage.getItem('activeTab') || 'machines';
    showTab(activeTab);

    document.getElementById('tab-machines').addEventListener('click', function() {
        showTab('machines');
    });

    document.getElementById('tab-maintenances').addEventListener('click', function() {
        showTab('maintenances');
    });

    document.getElementById('tab-reclamations').addEventListener('click', function() {
        showTab('reclamations');
    });

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

    function saveData(buttonId, tableId, url, dataMapping) {
        document.getElementById(buttonId).addEventListener('click', function() {
            let rows = document.querySelectorAll(`#${tableId} tbody tr`);
            let data = [];

            rows.forEach(row => {
                let rowData = {};
                dataMapping.forEach((mapping, index) => {
                    rowData[mapping] = row.cells[index].innerText.trim();
                });
                rowData.id = row.getAttribute('data-id');
                data.push(rowData);
            });

            console.log('Data to be sent:', JSON.stringify(data, null, 2));

            fetch(url, {
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
                    document.getElementById(buttonId).style.display = 'none';
                } else {
                    alert(`Произошла ошибка при сохранении изменений: ${data.message}`);
                }
            })
            .catch((error) => {
                console.error('Error:', error);
                alert('Произошла ошибка при сохранении изменений');
            });
        });
    }

    saveData('save-machines-button', 'machines', '/save_machines/', [
        'model_technique', 'serial_number', 'model_engine', 'model_transmission',
        'model_drive_axle', 'model_steering_axle', 'shipment_date'
    ]);

    saveData('save-maintenance-button', 'maintenances', '/save_maintenances/', [
        'maintenance_type', 'maintenance_date', 'operating_time', 'order_number', 'order_date'
    ]);

    saveData('save-reclamation-button', 'reclamations', '/save_reclamations/', [
        'failure_date', 'operating_time', 'failure_unit', 'recovery_method'
    ]);

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

    makeEditable('machines');
    makeEditable('maintenances');
    makeEditable('reclamations');

    function goToMachineDetail(machineId) {
        window.location.href = `/machine/${machineId}/`;
    }

    document.getElementById('machines').addEventListener('click', function(event) {
        if (event.target.tagName === 'TD') {
            var machineId = event.target.parentElement.getAttribute('data-id');
            goToMachineDetail(machineId);
        }
    });
});
