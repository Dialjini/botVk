var count = 100;
var tariff = 'Бизнес';
var time = 12;
var date0 = '?? апреля ????г. в ??:??';
var login = 'test';
var botname = 'test';
var crm = ''
var lkcrm = 'hz'
var apikey = '4t1278fbskd'


function main() {
    $.ajax({
        type: "GET",
        url: "/getForm",
        data: {'botname': botname, 'login': login}
    })
    .done(function(result) {
        console.log(result);
        console.log(JSON.parse(result));
        result = JSON.parse(result);
        date0 = result['date'];
        count = parseInt(result['balance']);
        time = result['count'];
        document.getElementById("date").innerHTML = date0;
        document.getElementById("count").innerHTML = count.toFixed(2) + " &#8381;";
        document.getElementById("countTo").innerHTML = count.toFixed(2) + " &#8381;";
        document.getElementById("tariff").innerHTML = tariff;
        document.getElementById("time").innerHTML = time;

    });

  //document.getElementById("count").innerHTML = count.toFixed(2) + " &#8381;";
 // document.getElementById("countTo").innerHTML = count.toFixed(2) + " &#8381;";
  //document.getElementById("tariff").innerHTML = tariff;
 // document.getElementById("time").innerHTML = time;

}

function checkBot(checkbox) {
if (checkbox.checked) {
    $.ajax({
        type: "GET",
        url: "/botStatus",
        data: {'botname': botname, 'login': login, 'mode': 'on'}
    })
    .done(function() {
        alert("Бот включен");
    });
} else {
 $.ajax({
        type: "GET",
        url: "/botStatus",
        data: {'botname': botname, 'login': login, 'mode': 'off'}
    })
    .done(function() {
        alert("Бот выключен");
    });
}
}

function settings() {
  $('.nav-item:first-child').addClass('active');
  $('.nav-item:last-child').removeClass('active');
  $('.settings').css('display', 'block');
  $('.card').css('display', 'none');
}

function card() {
  $('.nav-item:last-child').addClass('active');
  $('.nav-item:first-child').removeClass('active');
  $('.settings').css('display', 'none');
  $('.card').css('display', 'block');
}

function saveSettings(){

    var eMail = id('email').value;
    var lkcrm = id('linkCRM').value;
    var apikey = id('api-key').value;


    console.log(crm);

    if (eMail != "") {
      crm = eMail;
    }


    $.ajax({
        type: "GET",
        url: "/updateClient",
        data: {'botname': botname, 'login': login, 'crm': crm, 'lkcrm': lkcrm, 'apikey': apikey}
    })
    .done(function() {
        console.log('settings saved');
    });
}

function selectMode(selectObject) {
  crm = selectObject.value;
}

function id(id) {
  return document.getElementById(id);
}
