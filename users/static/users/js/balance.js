document.addEventListener('DOMContentLoaded', function () {
    function updateSum(prefix, excludeId, targetId) {
        var sum = 0;
        document.querySelectorAll(`input[id^="id_${prefix}"][id$="-value"]`).forEach(function (input) {
            if (input.id !== excludeId) {
                sum += parseFloat(input.value) || 0;
            }
        });
        document.getElementById(targetId).value = sum;
    }

    function updateSum2(prefix, excludeId, targetId) {
        var sum = 0;
        document.querySelectorAll(`input[id^="id_${prefix}"][id$="-value2"]`).forEach(function (input) {
            if (input.id !== excludeId) {
                sum += parseFloat(input.value) || 0;
            }
        });
        document.getElementById(targetId).value = sum;
    }

    function updateSum3(prefix, excludeId, targetId) {
        var sum = 0;
        document.querySelectorAll(`input[id^="id_${prefix}"][id$="-value3"]`).forEach(function (input) {
            if (input.id !== excludeId) {
                sum += parseFloat(input.value) || 0;
            }
        });
        document.getElementById(targetId).value = sum;
    }

    function update1600() {
        var sum = parseFloat(document.getElementById('id_1100-value').value) || 0;
        sum += parseFloat(document.getElementById('id_1200-value').value) || 0;
        document.getElementById('id_1600-value').value = sum;
    }

    function update16002() {
        var sum = parseFloat(document.getElementById('id_1100-value2').value) || 0;
        sum += parseFloat(document.getElementById('id_1200-value2').value) || 0;
        document.getElementById('id_1600-value2').value = sum;
    }

    function update16003() {
        var sum = parseFloat(document.getElementById('id_1100-value3').value) || 0;
        sum += parseFloat(document.getElementById('id_1200-value3').value) || 0;
        document.getElementById('id_1600-value3').value = sum;
    }

    function update1700() {
        var sum = parseFloat(document.getElementById('id_1300-value').value) || 0;
        sum += parseFloat(document.getElementById('id_1400-value').value) || 0;
        sum += parseFloat(document.getElementById('id_1500-value').value) || 0;
        document.getElementById('id_1700-value').value = sum;
    }

    function update17002() {
        var sum = parseFloat(document.getElementById('id_1300-value2').value) || 0;
        sum += parseFloat(document.getElementById('id_1400-value2').value) || 0;
        sum += parseFloat(document.getElementById('id_1500-value2').value) || 0;
        document.getElementById('id_1700-value2').value = sum;
    }

    function update17003() {
        var sum = parseFloat(document.getElementById('id_1300-value3').value) || 0;
        sum += parseFloat(document.getElementById('id_1400-value3').value) || 0;
        sum += parseFloat(document.getElementById('id_1500-value3').value) || 0;
        document.getElementById('id_1700-value3').value = sum;
    }

    function addChangeListeners(prefix, excludeId, targetId, sumFunction) {
        document.querySelectorAll(`input[id^="id_${prefix}"]`).forEach(function (input) {
            input.addEventListener("change", function () {
                sumFunction(prefix, excludeId, targetId);
                if (prefix === '11' || prefix === '12') {
                    update1600();
                    update16002();
                    update16003();
                }
                if (prefix === '13' || prefix === '14' || prefix === '15') {
                    update1700();
                    update17002();
                    update17003();
                }
            });
        });
    }

    // Adding listeners for value
    addChangeListeners('11', 'id_1100-value', 'id_1100-value', updateSum);
    addChangeListeners('12', 'id_1200-value', 'id_1200-value', updateSum);
    addChangeListeners('13', 'id_1300-value', 'id_1300-value', updateSum);
    addChangeListeners('14', 'id_1400-value', 'id_1400-value', updateSum);
    addChangeListeners('15', 'id_1500-value', 'id_1500-value', updateSum);// Adding listeners for value2
    addChangeListeners('11', 'id_1100-value2', 'id_1100-value2', updateSum2);
    addChangeListeners('12', 'id_1200-value2', 'id_1200-value2', updateSum2);
    addChangeListeners('13', 'id_1300-value2', 'id_1300-value2', updateSum2);
    addChangeListeners('14', 'id_1400-value2', 'id_1400-value2', updateSum2);
    addChangeListeners('15', 'id_1500-value2', 'id_1500-value2', updateSum2);

    // Adding listeners for value3
    addChangeListeners('11', 'id_1100-value3', 'id_1100-value3', updateSum3);
    addChangeListeners('12', 'id_1200-value3', 'id_1200-value3', updateSum3);
    addChangeListeners('13', 'id_1300-value3', 'id_1300-value3', updateSum3);
    addChangeListeners('14', 'id_1400-value3', 'id_1400-value3', updateSum3);
    addChangeListeners('15', 'id_1500-value3', 'id_1500-value3', updateSum3);
});

document.getElementById("id_date").addEventListener("change", updateTableHeaders);

function updateTableHeaders() {
    var selectedDate = new Date(document.getElementById("id_date").value); // Получаем выбранную дату
    var selectedYear = selectedDate.getFullYear(); // Получаем год из выбранной даты
    document.getElementById("selected_year").innerHTML = "Год " + selectedYear; // Обновляем заголовок для выбранного года
    document.getElementById("previous_year").innerHTML = "Год " + (selectedYear - 1); // Обновляем заголовок для предыдущего года
    document.getElementById("two_years_ago").innerHTML = "Год " + (selectedYear - 2); // Обновляем заголовок для года два года назад
}

function readFile() {
    const fileInput = document.getElementById('formFile');
    const file = fileInput.files[0];
    const reader = new FileReader();

    reader.onload = function(e) {
        const data = new Uint8Array(e.target.result);
        const workbook = XLSX.read(data, { type: 'array' });
        const firstSheetName = workbook.SheetNames[0];
        const worksheet = workbook.Sheets[firstSheetName];

        const jsonData = XLSX.utils.sheet_to_json(worksheet, { header: 1 });

        populateForm(jsonData);
    };

    reader.readAsArrayBuffer(file);
}
function populateForm(data) {
// Assume the data array structure matches the form structure
document.querySelector('input[name="company_name"]').value = data[1][0];

// Loop through indicators and populate their fields
const indicators = data.slice(3); // Adjust according to your data layout
indicators.forEach((row, index) => {
const formRow = document.querySelectorAll('tbody tr')[index];
formRow.querySelectorAll('td')[2].querySelector('input').value = row[2];
formRow.querySelectorAll('td')[3].querySelector('input').value = row[3];
formRow.querySelectorAll('td')[4].querySelector('input').value = row[4];
});

// Update sums after populating the form
update1600();
update16002();
update16003();
update1700();
update17002();
update17003();

// Add event listener to input fields to update sums automatically
const inputFields = document.querySelectorAll('input[type="number"]');
inputFields.forEach(input => {
input.addEventListener('change', function() {
const prefix = input.id.split('_')[1]; // Extract prefix from input id
const excludeId = input.id; // Exclude current input from sum calculation
let targetId;
if (prefix === '11' || prefix === '12') {
targetId = `id_1600-value${prefix === '11' ? '' : '2'}${prefix === '11' ? '' : '3'}`;
updateSum(prefix, excludeId, targetId);
} else if (prefix === '13' || prefix === '14' || prefix === '15') {
targetId = `id_1700-value${prefix === '13' ? '' : '2'}${prefix === '13' ? '' : '3'}`;
updateSum(prefix, excludeId, targetId);
}
});
});
}