$(document).ready(function () {
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
                success: function () {
                    //alert('URL captured');
                }
            })
        }
    });
});