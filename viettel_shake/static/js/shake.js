jQuery(function ($) {
  console.log('ready!');
  var $output = $('#output');
  var $form = $('#form');
  var $phone = $form.find('#phone');
  var $otp = $form.find('#otp');
  var $otpFormGroup = $otp.closest('div.form-group');

  var sentOTP = false;

  var CODE_SUCCESS = '00';
  var CODE_LOCKED = 'SG0004';

  var phoneNormalize = function (phone) {
    // remove prefix '0'
    // https://stackoverflow.com/a/8276474
    return phone.replace(/^0+/, '');
  };

  var requestLogin = function () {
    var payload = {
      'user_id': phoneNormalize($phone.val()),
    };
    axios.post(requestLoginPath, payload)
      .then(function (response) {
        var result = response.data;
        var status = result.status;
        var code = status.code;
        var message = status.message;
        console.log(result);
        console.log(code);
        console.log(message);
        // if send OTP success
        if (code === CODE_SUCCESS) {
          $('#phone').prop('disabled', true);
          $otpFormGroup.removeClass('d-none');
          sentOTP = true;
        } else if (code === CODE_LOCKED) {
          // account has been locked
          console.log('Account has been locked');
          var timeLeft = result.data.lockRemain;
          console.log('Time left: ' + timeLeft.toString())
        }
        $output.className = 'container';
        $output.innerHTML = result.status.message;
      })
      .catch(function (error) {
        $output.className = 'container text-danger';
        $output.innerHTML = error;
      });
  };

  var login = function () {
    var payload = {
      'user_id': phoneNormalize($phone.val()),
      'otp': $otp.val(),
    };
    axios.post(loginPath, payload)
      .then(function (response) {
        var data = response.data;
        console.log(data);
        console.log(data.status.code);
        console.log(data.status.message);
        // if send OTP success
        if (data.status.code === '00') {
          $('#phone').prop('disabled', true);
          $otpFormGroup.removeClass('d-none');
        }
        $output.className = 'container';
        $output.innerHTML = data.status.message;
      })
      .catch(function (error) {
        $output.className = 'container text-danger';
        $output.innerHTML = error;
      });
  };

  $form.submit(function (e) {
    e.preventDefault();
    if (!sentOTP) {
      requestLogin();
    } else {
      login();
    }
  });
});
