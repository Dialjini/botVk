var count = 1000000;
var tariff = 'Бизнес';
var time = 12;
var date0 = '?? апреля ????г. в ??:??';
//$.get("/getForm").done(function(result){
//        console.log(result)
//        date0 = result['date']
//    });
function main() {
    $.ajax({
        type: "GET",
        url: "/getForm",
        data: botname, login
    })
    .done(function(result) {
        console.log(result);
        date0 = result['date'];
    });
    });
  document.getElementById("count").innerHTML = count.toFixed(2) + " &#8381;";
  document.getElementById("countTo").innerHTML = count.toFixed(2) + " &#8381;";
  document.getElementById("tariff").innerHTML = tariff;
  document.getElementById("time").innerHTML = time;
  document.getElementById("date0").innerHTML = date0;
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
});

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
    $.get("/get").done(function(result){
    console.log(result);
    });
}