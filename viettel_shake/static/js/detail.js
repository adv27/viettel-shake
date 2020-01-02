jQuery(function ($) {
  var $table = $('#table');
  var $refresh = $('#refresh');

  var loadShakes = function (refresh = false) {
    axios.get(endpoint)
      .then(function (response) {
        var data = response.data;
        console.log(data);
        if (refresh) {
          // drop old rows then load new data
          $table.bootstrapTable('load', data.shakes);
          toastr.success('Updated!');
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
