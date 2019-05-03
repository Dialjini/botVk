var count = 100;
var tariff = 'Бизнес';
var time = 12;
var date0 = '?? апреля ????г. в ??:??';
var login = 'test';
var botname = 'test';
var crm = ''
var lkcrm = 'hz'
var apikey = '4t1278fbskd'


function getWidget() {
  $.ajax({
      type: "GET",
      url: "/getWidget",
    })
    .done(function(result) {
      alert(result);
    });

}

function main() {
  $.ajax({
      type: "GET",
      url: "/getForm",
      data: {
        'botname': botname,
        'login': login
      }
    })
    .done(function(result) {
      console.log(result);
      console.log(JSON.parse(result));
      result = JSON.parse(result);
      date0 = result['date'];
      count = parseInt(result['balance']);
      time = result['count'];
      id('date').innerHTML = date0;
      id('count').innerHTML = count.toFixed(2) + " &#8381;";
      id('countTo').innerHTML = count.toFixed(2) + " &#8381;";
      id('tariff').innerHTML = tariff;
      id('time').innerHTML = time;

    });

  //document.getElementById("count").innerHTML = count.toFixed(2) + " &#8381;";
  // document.getElementById("countTo").innerHTML = count.toFixed(2) + " &#8381;";
  //document.getElementById("tariff").innerHTML = tariff;
  // document.getElementById("time").innerHTML = time;

}

function checkBot(checkbox) {
  if (id('count').innerHTML) {
    if (checkbox.checked) {
      $.ajax({
          type: "GET",
          url: "/botStatus",
          data: {
            'botname': botname,
            'login': login,
            'mode': 'on'
          }
        })
        .done(function() {
          alert("Бот включен");
        });
    } else {
      $.ajax({
          type: "GET",
          url: "/botStatus",
          data: {
            'botname': botname,
            'login': login,
            'mode': 'off'
          }
        })
        .done(function() {
          alert("Бот выключен");
        });
    }
  } else {
    alert('Сначала введите свои данные, после чего нажмите кнопку "Сохранить"');
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

function saveSettings() {

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
      data: {
        'botname': botname,
        'login': login,
        'crm': crm,
        'lkcrm': lkcrm,
        'apikey': apikey
      }
    })
    .done(function() {
      console.log('settings saved');
    });
}

function selectMode(selectObject) {
  crm = selectObject.value;
  if (crm === 'email') {
    $('.email').fadeIn(1000);
    $('.linkCRM').fadeOut(100);
  } else {
    $('.email').fadeOut(100);
    $('.linkCRM').fadeIn(1000);
  }
}

function id(id) {
  return document.getElementById(id);
}
