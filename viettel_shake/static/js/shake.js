jQuery(function ($) {
  console.log('ready!');
  var $form = $('#form');
  var $phone = $form.find('#phone');
  var $otp = $form.find('#otp');
  var $otpFormGroup = $otp.closest('div.form-group');

  var sentOTP = false;

  var CODE_SUCCESS = '00';
  var CODE_LOCKED = 'SG0004';

  var REDIRECT_TIMEOUT = 1500;

  var requestLogin = function () {
    toastr.warning('Mã OPT đang được gửi đến điện thoại!');
    var payload = {
      'phone': $phone.val(),
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
          toastr.success(message);
        } else {
          switch (code) {
            case CODE_LOCKED: {
              // account has been locked
              console.log('Account has been locked');
              var timeLeft = result.data.lockRemain;
              console.log('Time left: ' + timeLeft.toString());
            }
          }
          toastr.error(message);
        }

      })
      .catch(function (error) {
        toastr.error(error, 'Error!')
      });
  };

  var login = function () {
    toastr.warning('Login!');
    var payload = {
      'phone': $phone.val(),
      'otp': $otp.val(),
    };
    axios.post(loginPath, payload)
      .then(function (response) {
        var result = response.data;
        var status = result.status;
        var code = status.code;
        var message = status.message;
        console.log(result);
        console.log(code);
        console.log(message);
        if (code === CODE_SUCCESS) {
          toastr.success(message, 'Đăng nhập');
          // redirect to histories page
          toastr.options.progressBar = true;
          toastr.warning('Đang chuyển hướng tới trang lịch sử...', '',{timeOut: REDIRECT_TIMEOUT});
          window.setTimeout(function () {
            window.location = '/detail/' + $phone.val();
          }, REDIRECT_TIMEOUT);
        } else {
          toastr.error(message);
        }
      })
      .catch(function (error) {
        toastr.error(error, 'Error!')
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
