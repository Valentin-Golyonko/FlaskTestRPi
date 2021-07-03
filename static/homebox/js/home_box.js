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
            console.log('common_data(): ajax_error; ', ajax_error);
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

function get_color_picker_value(light_up, light_off) {
    const current_color = $('#rgb_color_picker').val();
    const data_list = current_color.replace(
        'rgba(', ''
    ).replace(
        ')', ''
    ).split(
        ','
    );

    let color_data = {}

    if (light_up) {
        for (let i = 0; i < data_list.length; i++) {
            if (i === 0) {
                color_data['red'] = data_list[i]
            } else if (i === 1) {
                color_data['green'] = data_list[i]
            } else if (i === 2) {
                color_data['blue'] = data_list[i]
            } else if (i === 3) {
                color_data['alpha'] = data_list[i]
            } else {
                console.log('get_color_picker_value(): unknown i = ' + i)
            }
        }
    } else if (light_off) {
        color_data = {
            'red': 1,
            'green': 1,
            'blue': 1,
            'alpha': 1,
        }
    }

    return color_data
}

function send_color_to_rgb_strip(url_, csrf_token, login_url) {
    $("#light_up").on('click', function () {
        const color_data = get_color_picker_value(true, false);
        send_color_ajax(color_data, csrf_token, url_, login_url);
    })

    $("#light_off").on('click', function () {
        const color_data = get_color_picker_value(false, true);
        send_color_ajax(color_data, csrf_token, url_, login_url);
    })
}

function send_color_ajax(color_data, csrf_token, url_, login_url) {
    $.ajax({
        method: "POST",
        headers: {
            "Authorization": 'Bearer ' + sessionStorage.getItem('access'),
            "X-CSRFToken": csrf_token,
        },
        url: url_,
        data: color_data,
        dataType: 'json',
        success: function (response_data, textStatus, jqXHR) {
            console.log('send_color_ajax(): success; ', response_data, textStatus);
        },
        error: function (jqXHR, textStatus, errorThrown) {
            console.log('send_color_ajax(): error; ', textStatus, errorThrown);
            if (jqXHR.status === 401) {
                window.location.href = login_url;
            }
        },
    });
}