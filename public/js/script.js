var count = 100;
var tariff = 'Бизнес';
var time = 12;
var date0 = '?? апреля ????г. в ??:??';
var login = 'test';
var botname = 'test';
var crm = 'U-ON.Travel'
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
        document.getElementById("date").innerHTML = date0;
        document.getElementById("count").innerHTML = count.toFixed(2) + " &#8381;";

    });

  document.getElementById("count").innerHTML = count.toFixed(2) + " &#8381;";
  document.getElementById("countTo").innerHTML = count.toFixed(2) + " &#8381;";
  document.getElementById("tariff").innerHTML = tariff;
  document.getElementById("time").innerHTML = time;

}

function botStatus() {
    $.ajax({
        type: "GET",
        url: "/botStatus",
        data: $("#the-string input").val()
    })
    .done(function(result) {
        console.log("Bot is now" + result);
        botStatus = result
    });
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
        data: {'botname': botname, 'login': login, 'crm': crm, 'lkcrm': lkcrm, 'apikey': apikey}
    })
    .done(function() {
        console.log('settings saved');
    });
}
