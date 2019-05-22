var count = 100;
var tariff = '1 месяц';
var time = 12;
var date0 = '?? апреля ????г. в ??:??';
var login = 'test';
var botname = 'test';
var crm = '';
var lkcrm = 'hz';
var apikey = '4t1278fbskd';



function getWidget() {
  $.ajax({
      type: "GET",
      url: "/getWidget",
    })
    .done(function(result) {
      alert("Скопируйте ваш код виджета:\n" + result);
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
      login = result['login']
      date0 = result['date'];
      bot = result['botactive']
      if(bot === 'on') {
        checkbox.checked = true;
      }
      if(bot === 'off') {
        checkbox.checked = false;
      }

      var isnew = result['isnew'];

      VK.addCallback('onGroupSettingsChanged', function (mask, token){
      $.ajax({
      type: "GET",
      url: "/addPass",
      data: token
    })
    .done(function(result) {
       console.log(result)
    });})
      if (isnew === true) {
      VK.callMethod("showGroupSettingsBox", 8214+262144);
      }

      if (result['isnew'] != true){
        tariff = result['rate'];
        crm = result['crm'];
        lkcrm = result['lkcrm'];
        apikey = result['apikey'];

        count = parseInt(result['balance']);
        time = result['count'];
        id('crm').value = crm;
        if (crm === 'email') {
            id('email').value = lkcrm;
        } else {
            id('linkCRM').value = lkcrm;
        }
        id('api-key').value = apikey;
        id('date').innerHTML = date0;
        id('count').innerHTML = count.toFixed(2) + " &#8381;";
        id('countTo').innerHTML = count.toFixed(2) + " &#8381;";
        id('tariff').innerHTML = tariff;
        id('time').innerHTML = time;
        if (id('crm').value === 'email') {
           $('.email').fadeIn(1000);
           $('.linkCRM').fadeOut(0);
        }
        }
    });

  //document.getElementById("count").innerHTML = count.toFixed(2) + " &#8381;";
  // document.getElementById("countTo").innerHTML = count.toFixed(2) + " &#8381;";
  //document.getElementById("tariff").innerHTML = tariff;
  // document.getElementById("time").innerHTML = time;

}

function checkBot(checkbox) {
  if (id('count').innerHTML) {
    if (id('date').innerHTML.length < 54) {
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
      alert("Бот отключён. Пополните баланс.");
    }
  } else {
    alert('Сначала введите свои данные, после чего нажмите кнопку "Сохранить"');
  }
}

function settings() {
  $('.content').css('height', '');
  $('.nav-item:first-child').addClass('active');
  $('.nav-item:last-child').removeClass('active');
  $('.settings').css('display', 'block');
  $('.card').css('display', 'none');
}

function card() {
  $('.content').css('height', '910px');
  $('.nav-item:last-child').addClass('active');
  $('.nav-item:first-child').removeClass('active');
  $('.settings').css('display', 'none');
  $('.card').css('display', 'block');
}

function saveSettings() {

  var eMail = id('email').value;
  var lkcrm = id('linkCRM').value;
  var apikey = id('api-key').value;
  var count = id('count').innerHTML;

  console.log(crm);

  if (id("crm").value === "email") {
    lkcrm = eMail;
    crm = 'email';
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
      if (!id('count').innerHTML) {
        location.reload();
      }
      alert("Настройки сохранены");
    });
}

function selectMode(selectObject) {
  crm = selectObject.value;
  if (crm === 'email') {
    $('.email').fadeIn(1000);
    $('.linkCRM').fadeOut(0);
  } else {
    $('.email').fadeOut(1000);
    $('.linkCRM').fadeIn(0);
  }
}

function id(id) {
  return document.getElementById(id);
}
