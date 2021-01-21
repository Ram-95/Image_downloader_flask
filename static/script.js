$(document).ready(function () {
    /* Function to check if the provided URL is really IB URL.*/
    function is_valid_url_IB(url) {
        // Regular expression for: http://www.idlebrain.com/movie/photogallery/<Galleryname>/index.html
        return /^(http:\/\/)(www\.)?idlebrain.com\/movie\/photogallery\//.test(url);
    }

    $('.fetch').on('click', function () {
        url = $(".IB_url").val();
        //alert(is_valid_url(url));

        // If URL is not VALID, then alert the user.
        if (!is_valid_url_IB(url)) {
            alert('Invalid URL');
        }
        // Else continue with downloading images
        else {
            $('.notify').css('visibility', 'visible');
            $('.loader').css('display', '');
            $('.loader').css('visibility', 'visible');
            $('.status').css('color', 'blue');
            $('.status').text('Processing...');
            $.ajax({
                type: 'GET',
                url: '/IB',
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
                        $('.loader').css('display', 'none');
                        $('.status').css('color', 'green');
                        $('.status').text('Images downloaded and sent to your mail.');
                        $('.IB_url').val('');
                    }
                    else {
                        $('.loader').css('display', 'none');
                        $('.status').css('color', 'red');
                        $('.status').text('Invalid URL');
                    }
                }
            });
        }
    });
});