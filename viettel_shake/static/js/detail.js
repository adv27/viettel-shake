jQuery(function ($) {
  var $table = $('#table-history');
  var $refresh = $('#refresh');

  var loadShakes = function (refresh = false) {
    if (refresh) toastr.warning('Đang cập nhật...');

    axios.get(endpoint)
      .then(function (response) {
        var data = response.data;
        console.log(data);
        if (refresh) {
          // drop old rows then load new data
          $table.bootstrapTable('load', data.shakes);
          toastr.success('Đã cập nhật!');
        } else {
          // init table
          $table.bootstrapTable({data: data.shakes});
        }
      })
      .catch(function (error) {
        toastr.error(error, 'Error!')
      });
  };

  $refresh.click(function () {
    loadShakes(true);
  });

  loadShakes();
});
