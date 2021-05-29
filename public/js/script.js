function btn(e) {
    e.preventDefault();
}

var conVal = document.querySelector("#contrast");
var brightVal = document.querySelector("#brightness");
var conOut = document.querySelector("#contrastValue");
var brightOut = document.querySelector("#brightnessValue");
conOut.innerHTML = conVal.value;
brightOut.innerHTML = brightVal.value;

conVal.oninput = function () {
    conOut.innerHTML = conVal.value;
}
brightVal.oninput = function () {
    brightOut.innerHTML = brightVal.value;
}
var opt = document.getElementById("processVal");

function hide(x) {
    if(opt.value === '5') {
        document.querySelector("#brightness").disabled = false;
        document.querySelector("#contrast").disabled = false;
    }
    else {
        document.querySelector("#brightness").disabled = true;
        document.querySelector("#contrast").disabled = true;
    }
}
if (opt.value === '5') { 
    document.querySelector("#visible").disabled = false;
    document.querySelector("#contrast").disabled = false;
}
else {
    document.querySelector("#brightness").disabled = true;
    document.querySelector("#contrast").disabled = true;
}
