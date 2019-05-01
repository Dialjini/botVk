var count = 100;
var tariff = 'Бизнес';
var time = 12;
var date0 = '?? апреля ????г. в ??:??';
var crm = 'U-ON.Travel';
var lkcrm = 'hz';
var apikey = '4t1278fbskd';

class User {
    constructor() {
        this.login = 'test';
        this.botname = 'test';
    }
}
let user = new User;

$.ajax({
    type: "GET",
    url:"/"
})
.done(function(result) {
    result = JSON.parse(result);
    user.login = result['login'];
    user.botname = result['botname'];
});


function main() {
    $.ajax({
        type: "GET",
        url: "/getForm",
        data: {'login': user.login, 'botname': user.botname}
    })
    .done(function(result) {
        result = JSON.parse(result);
        date0 = result['date'];
        count = parseInt(result['balance']);
        document.getElementById("date").innerHTML = date0;
        document.getElementById("count").innerHTML = count.toFixed(2) + " &#8381;";

    });

  document.getElementById("count").innerHTML = count.toFixed(2) + " &#8381;";
  document.getElementById("countTo").innerHTML = count.toFixed(2) + " &#8381;";
  document.getElementById("tariff").innerHTML = tariff;
  document.getElementById("time").innerHTML = time;

}

function checkBot(checkbox) {
if (checkbox.checked) {
    $.ajax({
        type: "GET",
        url: "/botStatus",
        data: {'mode': 'on', 'login': user.login, 'botname': user.botname}
    })
    .done(function() {
        alert("Бот включен");
    });
} else {
 $.ajax({
        type: "GET",
        url: "/botStatus",
        data: {'mode': 'off', 'login': user.login, 'botname': user.botname}
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

    $.ajax({
        type: "GET",
        url: "/updateClient",
        data: {'crm': crm, 'lkcrm': lkcrm, 'apikey': apikey, 'login': user.login, 'botname': user.botname}
    })
    .done(function() {
        console.log('settings saved');
    });
}
