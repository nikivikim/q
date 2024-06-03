function calculateSums() {
var sum_1100 = 0;
var sum_1200 = 0;
var sum_1300 = 0;
var sum_1400 = 0;
var sum_1500 = 0;

var inputs = document.querySelectorAll('.indicator-input');
inputs.forEach(function(input) {
var value = parseFloat(input.value);
if (!isNaN(value)) {
var code = input.name.split('_')[1];
if (code.startsWith('11') && code !=='1100') {
sum_1100 += value;
} else if (code.startsWith('12') && code !=='1200') {
sum_1200 += value;
} else if (code.startsWith('13') && code !=='1300') {
sum_1300 += value;
} else if (code.startsWith('14') && code !=='1400') {
sum_1400 += value;
} else if (code.startsWith('15') && code !=='1500') {
sum_1500 += value;
}
}
});

document.querySelector('input[name="indicator_1100"]').value = sum_1100;
document.querySelector('input[name="indicator_1200"]').value = sum_1200;
document.querySelector('input[name="indicator_1300"]').value = sum_1300;
document.querySelector('input[name="indicator_1400"]').value = sum_1400;
document.querySelector('input[name="indicator_1500"]').value = sum_1500;
}

function calc() {
calculateSums();
var currentLiquidity = parseFloat(document.querySelector('input[name="indicator_1200"]').value) / parseFloat(document.querySelector('input[name="indicator_1500"]').value);
var absoluteLiquidity = (parseFloat(document.querySelector('input[name="indicator_1200"]').value) + parseFloat(document.querySelector('input[name="indicator_1300"]').value)) / parseFloat(document.querySelector('input[name="indicator_1500"]').value);
var quickLiquidity = (parseFloat(document.querySelector('input[name="indicator_1200"]').value) + parseFloat(document.querySelector('input[name="indicator_1300"]').value) + parseFloat(document.querySelector('input[name="indicator_1400"]').value)) / parseFloat(document.querySelector('input[name="indicator_1500"]').value);

var tableHTML = '<table class="table"><tbody>';
tableHTML += '<tr><td>Текущая ликвидность</td><td>' + currentLiquidity + '</td></tr>';
tableHTML += '<tr><td>Абсолютная ликвидность</td><td>' + absoluteLiquidity + '</td></tr>';
tableHTML += '<tr><td>Быстрая ликвидность</td><td>' + quickLiquidity + '</td></tr>';
tableHTML += '</tbody></table>';

document.getElementById('liquidityTable').innerHTML = tableHTML;

var period = document.getElementById('yearHeader').textContent;
renderLiquidityChart([currentLiquidity, absoluteLiquidity, quickLiquidity], period);
}

function buildReport() {
var sum_1200 = parseFloat(document.querySelector('input[name="indicator_1200"]').value);
var sum_1300 = parseFloat(document.querySelector('input[name="indicator_1300"]').value);
var sum_1400 = parseFloat(document.querySelector('input[name="indicator_1400"]').value);
var sum_1500 = parseFloat(document.querySelector('input[name="indicator_1500"]').value);
var a_1 = parseFloat(document.querySelector('input[name="indicator_1240"]').value)+parseFloat(document.querySelector('input[name="indicator_1250"]').value);
var a_2 = parseFloat(document.querySelector('input[name="indicator_1230"]').value);
console.log(a_1)
var currentLiquidity = sum_1200 / sum_1500;
var absoluteLiquidity = a_1 / sum_1500;
var quickLiquidity =(a_1+a_2)/ sum_1500;

var liquidityData = [currentLiquidity, absoluteLiquidity, quickLiquidity];

renderLiquidityChart(liquidityData);
}

document.addEventListener('DOMContentLoaded', function() {
var inputs = document.querySelectorAll('.indicator-input');
inputs.forEach(function(input) {
input.addEventListener('input', function() {
calculateSums();
});
});
var container = document.getElementById('yearSelectorContainer');
for (var year = 2023; year >= 1990; year--) {
    var option = document.createElement('option');
    option.value = year;
    option.textContent = year;
    container.appendChild(option);
}

var yearSelector = document.getElementById('yearSelectorContainer');
yearSelector.addEventListener('change', function() {
    var selectedYear = parseInt(yearSelector.value);
});

var yearHeader = document.getElementById('yearHeader');
yearHeader.textContent = 'За 31.12. ' + container.value;
container.addEventListener('change', function() {
    yearHeader.textContent = 'За 31.12.' + container.value;
});

});
var myChart; // Глобальная переменная для хранения объекта графика

function renderLiquidityChart(liquidityData, period) {
    var ctx = document.getElementById('liquidityChart').getContext('2d');
    var labels = ["Текущая ликвидность", "Абсолютная ликвидность", "Быстрая ликвидность"];

    // Если график уже существует, удаляем его
    if (myChart) {
        myChart.destroy();
    }

    myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: period,
                data: liquidityData,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                ],
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}
function readFile() {
    var fileInput = document.getElementById('formFile');
    if (fileInput.files.length === 0) {
        alert("Выберите файл Excel для загрузки.");
        return;
    }

    var file = fileInput.files[0];
    var reader = new FileReader();

    reader.onload = function(event) {
        var data = event.target.result;
        var workbook = XLSX.read(data, { type: 'array' });
        var firstSheetName = workbook.SheetNames[0];
        var firstSheet = workbook.Sheets[firstSheetName];

        // Пример чтения данных из ячеек и заполнения полей ввода с проверкой на существование ячейки
        var startRow1 = 1; // Начальная строка для первого диапазона (1110 - 1190)
var endRow1 = 9; // Конечная строка для первого диапазона

for (var i = startRow1; i <= endRow1; i++) {
    var cellAddress1 = 'A' + i;
    if (firstSheet[cellAddress1] !== undefined && firstSheet[cellAddress1].v !== undefined) {
        var cellValue1 = firstSheet[cellAddress1].v;
        var indicatorId1 = 1110 + (i - startRow1) * 10; // Вычисляем идентификатор индикатора на основе текущей строки
        document.querySelector('input[name="indicator_' + indicatorId1 + '"]').value = cellValue1;
    } else {
        console.error("Ячейка " + cellAddress1 + " не найдена или не содержит значения.");
    }
}

var startRow2 = 10; // Начальная строка для второго диапазона (1210 - 1260)
var endRow2 = 15; // Конечная строка для второго диапазона

for (var j = startRow2; j <= endRow2; j++) {
    var cellAddress2 = 'A' + j;
    if (firstSheet[cellAddress2] !== undefined && firstSheet[cellAddress2].v !== undefined) {
        var cellValue2 = firstSheet[cellAddress2].v;
        var indicatorId2 = 1210 + (j - startRow2) * 10; // Вычисляем идентификатор индикатора на основе текущей строки
        document.querySelector('input[name="indicator_' + indicatorId2 + '"]').value = cellValue2;
    } else {
        console.error("Ячейка " + cellAddress2 + " не найдена или не содержит значения.");
    }
}

var startRow3 = 16; // Начальная строка для третьего диапазона (1210 - 1260)
var endRow3 = 22; // Конечная строка для третьего диапазона

for (var j = startRow3; j <= endRow3; j++) {
    var cellAddress3 = 'A' + j;
    if (firstSheet[cellAddress3] !== undefined && firstSheet[cellAddress3].v !== undefined) {
        var cellValue3 = firstSheet[cellAddress3].v;
        var indicatorId3 = 1310 + (j - startRow3) * 10; // Вычисляем идентификатор индикатора на основе текущей строки

        // Проверяем, существует ли индикатор с этим идентификатором
        var indicatorElement = document.querySelector('input[name="indicator_' + indicatorId3 + '"]');
        if (indicatorElement !== null) {
            indicatorElement.value = cellValue3;
        } else {
            console.error("Индикатор с идентификатором " + indicatorId3 + " не найден.");
        }
    } else {
        console.error("Ячейка " + cellAddress3 + " не найдена или не содержит значения.");
    }
}
var startRow4 = 23; // Начальная строка для третьего диапазона (1210 - 1260)
var endRow4 = 27; // Конечная строка для третьего диапазона

for (var j = startRow4; j <= endRow4; j++) {
    var cellAddress4 = 'A' + j;
    if (firstSheet[cellAddress4] !== undefined && firstSheet[cellAddress4].v !== undefined) {
        var cellValue4 = firstSheet[cellAddress4].v;
        var indicatorId4 = 1410 + (j - startRow4) * 10; // Вычисляем идентификатор индикатора на основе текущей строки

        // Проверяем, существует ли индикатор с этим идентификатором
        var indicatorElement = document.querySelector('input[name="indicator_' + indicatorId4 + '"]');
        if (indicatorElement !== null) {
            indicatorElement.value = cellValue4;
        } else {
            console.error("Индикатор с идентификатором " + indicatorId4 + " не найден.");
        }
    } else {
        console.error("Ячейка " + cellAddress4 + " не найдена или не содержит значения.");
    }
}
var startRow5 = 28; // Начальная строка для третьего диапазона (1210 - 1260)
var endRow5 = 32; // Конечная строка для третьего диапазона

for (var j = startRow5; j <= endRow5; j++) {
    var cellAddress5 = 'A' + j;
    if (firstSheet[cellAddress5] !== undefined && firstSheet[cellAddress5].v !== undefined) {
        var cellValue5 = firstSheet[cellAddress5].v;
        var indicatorId5 = 1510 + (j - startRow5) * 10; // Вычисляем идентификатор индикатора на основе текущей строки

        // Проверяем, существует ли индикатор с этим идентификатором
        var indicatorElement = document.querySelector('input[name="indicator_' + indicatorId5 + '"]');
        if (indicatorElement !== null) {
            indicatorElement.value = cellValue5;
        } else {
            console.error("Индикатор с идентификатором " + indicatorId5 + " не найден.");
        }
    } else {
        console.error("Ячейка " + cellAddress5 + " не найдена или не содержит значения.");
    }
}

    };

    reader.readAsArrayBuffer(file);
}

function analyzeData() {
    // Получаем CSRF-токен из куки
    const csrftoken = getCookie('csrftoken');

    // Получаем значения из полей ввода
    var inputData = {};
    var inputFields = document.querySelectorAll('.indicator-input');
    inputFields.forEach(function(field) {
        inputData[field.name] = field.value;
    });

    // Отправляем запрос на сервер для проведения анализа
    fetch('analyze_data/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken  // Включаем CSRF-токен в заголовки запроса
        },
        body: JSON.stringify(inputData) // Передаем данные из полей ввода
    })
    .then(response => response.json())
    .then(data => {
        // После получения ответа от сервера выводим результаты анализа
        document.getElementById('analysisResults').innerHTML = data.result;
    })
    .catch(error => {
        console.error('Ошибка:', error);
    });
}

// Функция для получения CSRF-токена из куки
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.getElementById('analyzeButton').addEventListener('click', analyzeData);