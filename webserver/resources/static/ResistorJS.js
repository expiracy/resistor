// defining commonly used elements
const select_input = document.getElementById('select_input');
const canvas = document.getElementById('canvas_id');

//defining variables
var image = new Image();
var dragging = false;
var target = null;
var snapshot = null;

// defining resistor variables
var resistor = null
var resistor_bands = [];
var resistor_type = 6;

// defining button tracking variables
var button_presses = [];
var band_presses = [];

// picture canvas
var context = canvas.getContext('2d');
context.strokeStyle = 'green';
context.lineWidth = 3;
context.lineCap = 'round';

// event listener to track mouse position
canvas.addEventListener('mousedown', dragStart, false);
canvas.addEventListener('mousemove', drag, false);
canvas.addEventListener('mouseup', dragStop, false);

canvas.addEventListener('touchstart', dragStart, false);
canvas.addEventListener('touchmove', drag, false);
canvas.addEventListener('touchend', dragStop, false);

// simulate button click
function clickButton(element_id) {
    document.getElementById(element_id).click();
}

function drawFileAndShowScanButton() {
    file = select_input.files[0];
    drawFile(file);
    document.getElementById('scan_button').style.display = 'inline'
}

function uploadFile() {
    // getting uploaded file and its location
    file = select_input.files[0];
    uploadAndResponse(file, target);
}

function uploadAndResponse(file, position) {
    // creating variables for ajax
    var form = new FormData();
    var xhr = new XMLHttpRequest();

    // setting the x and y positions
    x = position.x * image.width / canvas.width
    y = position.y * image.height / canvas.height

    // posting the values to flask
    form.append('x', x)
    form.append('y', y)
    form.append('file', file);
    xhr.open('post', '/api', true);
    xhr.send(form);

    // responses to the ajax post
    xhr.onreadystatechange = function () {
        if (xhr.readyState === XMLHttpRequest.DONE) {

            resistor = JSON.parse(xhr.responseText)

            var resistor_bands = resistor['bands'];
            var number_of_bands = resistor['type'];

            console.log(resistor)
            console.log(number_of_bands)

            // calculating values for resistor
            resistorType(number_of_bands)
            outputResistorValues(processResistor(resistor_bands[0], resistor_bands[1], resistor_bands[2], resistor_bands[3], resistor_bands[4], resistor_bands[5]))

            // selecting bands
            var index = 0;

            for (; index < resistor_bands.length; index++) {
                bandButtonSelected(index + 1, resistor_bands[index])
            }
        }
    }
}


function drawFile(file) {
    var reader = new FileReader();

    reader.onload = function (e) {
      var dataURL = e.target.result,
          ctx = canvas.getContext('2d')

      image.onload = function() {
        width = window.innerWidth
            || document.documentElement.clientWidth
            || document.body.clientWidth;

        canvas.width = width * 3 / 4
        canvas.height = canvas.width * 3 / 4;
        context.drawImage(image, 0, 0, image.width, image.height, 0, 0,  canvas.width,  canvas.height);
        takeSnapshot()
        target =  { x: (canvas.width / 2), y: (canvas.height / 2) }
        drawCircle(target)
      };
      image.src = dataURL;
    };

    reader.readAsDataURL(file);
  }

function getCanvasCoordinates(event) {
    var x = event.clientX - canvas.getBoundingClientRect().left,
        y = event.clientY - canvas.getBoundingClientRect().top;

    return {x: x, y: y};
}

function takeSnapshot() {
    snapshot = context.getImageData(0, 0, canvas.width, canvas.height);
}

function restoreSnapshot() {
    context.putImageData(snapshot, 0, 0);
}


function drawCircle(position) {
    var radius = 20
    context.beginPath();
    context.strokeStyle = '#00FF00'
    context.lineWidth = 3
    context.shadowBlur = 5;
    context.shadowColor = 'BLACK';
    context.arc(position.x, position.y, radius, 0, 2 * Math.PI);
    context.stroke();
}


function dragStart(event) {
    dragging = true;
    restoreSnapshot();
    target = getCanvasCoordinates(event);
    drawCircle(target);
}


function drag(event) {
    if (dragging === true) {
        restoreSnapshot();
        target = getCanvasCoordinates(event);
        drawCircle(target);
    }
}


function dragStop(event) {
    dragging = false;
    restoreSnapshot();
    target = getCanvasCoordinates(event);
    drawCircle(target);
}


function stopBandButtonSelected(element_id) {
    try {
        document.getElementById(element_id).classList.remove('add_selected');
    }
    catch {
        console.log("Deselected a button that doesn't exist.")
    }
}


function addBandButtonSelected(element_id) {
    try {
        document.getElementById(element_id).className += ' add_selected';
    }
    catch {
        console.log("Button for this colour does not exist on this band.")
    }
}


function checkBandPressDupes(band, colour) {
    if (band_presses.includes(band)) {

        var index = band_presses.indexOf(band);
        var dupe_flash_element = button_presses[index];

        delete button_presses[index];
        delete band_presses[index];

        stopBandButtonSelected(dupe_flash_element);
    }
}


function findElementId(band, colour) {
    band.toString()

    var element_target = ('_' + band + '_' + colour)

    return 'band_button' + element_target;
}


function bandButtonSelected(band, colour) {
    var element_id = findElementId(band, colour);

    checkBandPressDupes(band, colour);

    button_presses.push(element_id);
    band_presses.push(band);

    addBandButtonSelected(element_id)
}


function bandButtonPress(band, colour) {
    bandButtonSelected(band, colour)

    if (band == 1) {
        resistor_bands[0] = colour
    }

    if (band == 2) {
        resistor_bands[1] = colour
    }

    if (band == 3) {
        resistor_bands[2] = colour
    }

    if (band == 4) {
        resistor_bands[3] = colour

    }

    if (band == 5) {
        resistor_bands[4] = colour

    }

    if (band == 6) {
        resistor_bands[5] = colour
    }

    outputResistorValues(processResistor(resistor_bands[0], resistor_bands[1], resistor_bands[2], resistor_bands[3], resistor_bands[4], resistor_bands[5]))
}

function getDigits(band_1, band_2, band_3) {
    var digits = {
        'BLACK':'0',
        'BROWN':'1',
        'RED':'2',
        'ORANGE':'3',
        'YELLOW':'4',
        'GREEN':'5',
        'BLUE':'6',
        'VIOLET':'7',
        'GREY':'8',
        'WHITE':'9'
    }

    var digit_1 = digits[band_1]
    var digit_2 = digits[band_2]
    var digit_3 = digits[band_3]

    if (typeof digit_1 === 'undefined') {
        digit_1 = ''
    }

    if (typeof digit_2 === 'undefined') {
        digit_2 = ''
    }

    if (typeof digit_3 === 'undefined') {
        digit_3 = ''
    }

    return digit_1 + digit_2 + digit_3
}

function getMultiplier(colour) {
    var multipliers = {
        'BLACK':1,
        'BROWN':10,
        'RED':100,
        'ORANGE':1000,
        'YELLOW':10000,
        'GREEN':100000,
        'BLUE':1000000,
        'VIOLET':10000000,
        'GREY':100000000,
        'WHITE':1000000000,
        'GOLD':0.1,
        'SILVER':0.01
    }

    var multiplier = multipliers[colour]

    if (typeof multiplier === 'undefined') {
        var multiplier = 1
    }

    return multiplier
}


function getTolerance(colour) {
    var tolerances = {
        'BLACK':0,
        'BROWN':1,
        'RED':2,
        'ORANGE':3,
        'YELLOW':4,
        'GREEN':0.5,
        'BLUE':0.25,
        'VIOLET':0.1,
        'GREY':0.05,
        'GOLD':5,
        'SILVER':10
    }

    if (typeof tolerances[colour] === 'undefined') {
        return undefined
    }

    return tolerances[colour]

}


function getTemperatureConstant(colour) {
    var temperature_constants = {
        'BLACK':0,
        'BROWN':100,
        'RED':50,
        'ORANGE':15,
        'YELLOW':25,
        'BLUE':10,
        'VIOLET':5
    }

    if (typeof temperature_constants[colour] === 'undefined') {
        return undefined
    }

    return temperature_constants[colour]
}


function processResistor(band_1, band_2, band_3, band_4, band_5, band_6) {
    var digits = getDigits(band_1, band_2, band_3);
    var multiplier = getMultiplier(band_4);
    var tolerance = getTolerance(band_5);
    var temperature_constant = getTemperatureConstant(band_6);

    var resistance = digits * multiplier;

    return [resistance, tolerance, temperature_constant]

}


function removeTableColumns(band_amount) {
    deselectColumns()

    var inactive_bands = {
        3:['band_3', 'band_5', 'band_6'],
        4:['band_3', 'band_6'],
        5:['band_6']
    }

    var index = 0;

    var remove_columns = inactive_bands[band_amount];

    for (; index < remove_columns.length; index++) {

        document.getElementById(remove_columns[index]).style.display = 'none';
        document.getElementById(remove_columns[index] + '_header').style.display = 'none';
    }
}


function addTableColumns(band_amount) {
    var columns_for_band = {
        3:['band_1', 'band_2', 'band_4'],
        4:['band_1', 'band_2', 'band_4', 'band_5'],
        5:['band_1', 'band_2', 'band_3', 'band_4', 'band_5'],
        6:['band_1', 'band_2', 'band_3', 'band_4', 'band_5', 'band_6']
    }

    var index = 0;

    var add_columns = columns_for_band[band_amount];

    for (; index < add_columns.length; index++) {

        document.getElementById(add_columns[index]).style.display = '';
        document.getElementById(add_columns[index] + '_header').style.display = '';
    }
}


function resistorType(band_amount) {
    if (band_amount < resistor_type) {

        removeTableColumns(band_amount);
        resistor_type = band_amount;
    }

    else {
        addTableColumns(band_amount);
        resistor_type = band_amount;
    }
}

function deselectColumns() {
    var index = 0;

    for (; index < button_presses.length; index++) {

        if (typeof button_presses[index] !== 'undefined') {

            var element_id = button_presses[index];

            try {
                document.getElementById(element_id).classList.remove('add_selected');
            }
            catch {
                console.log("Deselected a button that doesn't exist.")
            }
        }
    }

    resistor_bands = [];
    button_presses = [];
    band_presses = [];

    // recalculating the resistance after a column is deselected
    outputResistorValues(processResistor(resistor_bands[0], resistor_bands[1], resistor_bands[2], resistor_bands[3], resistor_bands[4], resistor_bands[5]))
}

function outputResistorValues(resistor_value) {
    // outputting the resistance by updating HTML for specific elements
    document.getElementById('resistance').innerText = 'Resistor: ' + resistor_value[0] + 'Ω';
    document.getElementById('tolerance').innerText = 'Tolerance +-: ' + resistor_value[1] + '%';
    document.getElementById('temperature_constant').innerText = 'Temperature Constant: ' + resistor_value[2] + 'ppm/K';

    // hiding the elements if no values are present
    if (resistor_value[0] === 0) {
        document.getElementById('resistance').innerText = '';
    }

    if (typeof resistor_value[1] === 'undefined') {
        document.getElementById('tolerance').innerText = '';
    }

    if (typeof resistor_value[2] === 'undefined') {
        document.getElementById('temperature_constant').innerText = '';
    }
}


