$(document).ready(function () {
    var gallery = ''
    $('.fetch').on('click', function () {
        url = $(".IB_url").val();
        if (url == '') {
            alert('Invalid URL');
        }
        else {
            /*
            $('.notify').css('visibility', 'visible');
            $('.status').text('Downloading status..');
            */
            //alert(url);
            $.ajax({
                type: 'GET',
                url: '/',
                cache: false,
                data: {
                    url: url,
                },
                success: function (data) {
                    //alert('URL captured');
                    $('.download_section').css('visibility', 'visible');
                    gallery = data;
                }
            });
        }
    });

    $('.download_btn').on('click', function () {
        location.href = gallery;
    });
});