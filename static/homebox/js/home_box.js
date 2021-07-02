function get_common_choices(url_) {
    $.ajax({
        method: "GET",
        url: url_,
        data: {
            q: 'device_type_choices,device_sub_type_choices,device_address_type_choices,forecast_units_choices',
        },
        dataType: 'json',
        success: function (ajax_data) {
            sessionStorage.setItem(
                'device_type_choices', JSON.stringify(ajax_data.device_type_choices)
            );
            sessionStorage.setItem(
                'device_sub_type_choices', JSON.stringify(ajax_data.device_sub_type_choices)
            );
            sessionStorage.setItem(
                'device_address_type_choices', JSON.stringify(ajax_data.device_address_type_choices)
            );
            sessionStorage.setItem(
                'forecast_units_choices', JSON.stringify(ajax_data.forecast_units_choices)
            );
        },
        error: function (ajax_error) {
            console.log('common_data | ajax_error', ajax_error);
        },
    });
}

function set_common_choices_str(choice_obj, common_choices, str_id, str_name) {
    JSON.parse(
        choice_obj
    ).forEach(
        (element) => {
            let set_str;
            if (element.key === common_choices) {
                set_str = element.label
            } else {
                set_str = '-'
            }
            $('#' + str_id).text(str_name + ': ' + set_str)
        }
    );
}

function get_color_picker_value() {
    $("#send_color").on('click', function () {
        const current_color = $('#rgb_color_picker').data('current-color');
        console.log('current-color: ', current_color);
        const data_list = current_color.replace('rgba(', '').replace(')', '').split(',');
        console.log('data_list: ', data_list);
    })
}