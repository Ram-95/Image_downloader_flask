$(document).ready(function () {

    /* Function to check if the provided URL is really IB URL.*/
    function is_valid_url_IB(url) {
        // Regular expression for: http://www.idlebrain.com/movie/photogallery/<Galleryname>/index.html
        return /^(http:\/\/)(www\.)?idlebrain.com\/movie\/photogallery\//.test(url);
    }

    function is_valid_url_RG(url) {
        /* m.ragalahari.com -- is for mobile. So accept if url has either www./m.  */
        return /^(http(s)?:\/\/)((www|m)\.)?ragalahari.com\/(movie(s)?|actor|actress|localevents)\//.test(url);
    }

    function is_valid_url_CJ(url) {
        /*  common: https://www.cinejosh.com/gallery-thumbs */
        return /^(http(s)?:\/\/)(www\.)?cinejosh.com\/(gallery-thumbs)\//.test(url);
    }

    function is_valid_url_BS(url) {
        // Tollywoodhq
        tq = /^(http(s)?:\/\/)(www\.)?tollywoodhq.com/.test(url);
        // Sumon4all
        s4 = /^(http:\/\/)(www\.)?sumon4all.blogspot.com/.test(url);
        // Blogspot
        bs = /^(http:\/\/)(www\.)[a-zA-Z0-9]*\.[blogspot.com]/.test(url);
        
        return tq || s4 || bs;
    }

    /* Function that does some CSS manipulation when given URL is valid */
    function if_valid_url() {
        $('.notify').css('visibility', 'visible');
        $('.loader').css('display', '');
        $('.loader').css('visibility', 'visible');
        $('.status').css('color', 'blue');
        $('.status').text('Processing...');
    }

    function if_invalid_url() {
        alert('Invalid URL');
    }

    function if_ajax_invalid_url() {
        $('.loader').css('display', 'none');
        $('.status').css('color', 'red');
        $('.status').text('Invalid URL/Not Found');
    }

    function if_ajax_valid_url() {
        $('.loader').css('display', 'none');
        $('.status').css('color', 'green');
        $('.status').text('Images downloaded and sent to your mail.');
    }

    function ajax_function(url) {
        $.ajax({
            type: 'GET',
            url: '/' + site,
            cache: false,
            data: {
                url: url,
            },
            success: function (data) {
                /*
                'data' is the INVALID_URL status from the backend. If INVALID_URL == 'True', then show 'Invlalid URL'
                else Download the images
                */
                //alert(data);
                if (data == 'False') {
                    if_ajax_valid_url();
                    $('.IB_url').val('');
                }
                else {
                    if_ajax_invalid_url();
                }
            }
        });
    }

    /* Sending Data to backend Functionality */
    $('.fetch').on('click', function () {
        site = $(this).attr("id");
        //alert('Site: ' + site);
        url = $("." + site + "_url").val();
        //alert(is_valid_url(url));

        /* Idlebrain */
        if (site == 'IB') {
            if (!is_valid_url_IB(url)) {
                if_invalid_url();
            }
            else {
                if_valid_url();
                ajax_function(url);
            }
        }
        /* Ragalahari */
        else if (site == 'RG') {
            if (!is_valid_url_RG(url)) {
                if_invalid_url();
            }
            else {
                if_valid_url();
                ajax_function(url);
            }
        }
        /* Cinejosh */
        else if (site == 'CJ') {
            if (!is_valid_url_CJ(url)) {
                if_invalid_url();
            }
            else {
                if_valid_url();
                ajax_function(url);
            }
        }
        /* Blospot/s4all/Tollywoodhq */
        else if (site == 'BS') {
            if (!is_valid_url_BS(url)) {
                if_invalid_url();
            }
            else {
                if_valid_url();
                ajax_function(url);
            }
        }

    });
});