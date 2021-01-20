$(document).ready(function () {
    var gallery = ''
    $('.fetch').on('click', function () {
        url = $(".IB_url").val();
        if (url == '') {
            alert('Invalid URL');
        }
        else {
            $('.notify').css('visibility', 'visible');
            $('.loader').css('visibility', 'visible');
            $('.status').text('Processing...');
            $.ajax({
                type: 'GET',
                url: '/',
                cache: false,
                data: {
                    url: url,
                },
                success: function (data) {
                    //alert('URL captured');
                    $('.loader').css('display', 'none');
                    $('.status').text('Images downloaded and sent to your mail.');
                    $('.IB_url').val('');
                }
            });
        }
    });
});