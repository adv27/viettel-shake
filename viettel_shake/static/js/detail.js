jQuery(function ($) {
    var $table = $('#table-history');
    var $refresh = $('#refresh');

    function calData(shakes) {
        console.log(shakes)

        return [...shakes
            .sort((a,b)=>a.data.status.code > b.data.status.code ? 1 : -1)
            .map((shake)=>{
            let res = {...shake};
            if(shake.data.status.code !== "SG0023"){
                res.data.status.code = shake.data.data.name;
                console.log(shake.data.data)
            }else {
                res.data.status.code = 'FAIL';
            }
            return res;
        })];
    }

    var loadShakes = function (refresh = false) {
        if (refresh) toastr.warning('Đang cập nhật...');

        axios.get(endpoint)
            .then(function (response) {
                var data = response.data;
                console.log(data);
                if (refresh) {
                    // drop old rows then load new data
                    $table.bootstrapTable('load', calData(data.shakes));
                    toastr.success('Đã cập nhật!');
                } else {
                    // init table
                    $table.bootstrapTable({data: calData(data.shakes)});
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
