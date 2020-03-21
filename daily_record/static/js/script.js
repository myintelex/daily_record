$(document).ready(function () {
    $('#nav-score').html('<i class="fa fa-line-chart"></i> &nbsp;<b><i class="fa fa-refresh fa-spin"></i> </i></b>')
    $('#month-score').html('<i class="fa fa-ellipsis-h"></i>')
    $('#prev-month-score').html('<i class="fa fa-ellipsis-h "></i>')

    DailyRecordApp.refreshScore()
    DailyRecordApp.showHabitList()
    // DailyRecordApp.showHabitCharts()
    $(document).on('click', '#btn-habit-list', function () {
        DailyRecordApp.showHabitList()
    })
    $(document).on('click', '#btn-habit-charts', function () {
        DailyRecordApp.showHabitCharts()
    })
    $('.circle').each(function (index, el) {
        var num = $(this).find('span').text() * 3.6;
        if (num <= 180) {
            $(this).find('.right').css('transform', "rotate(" + num + "deg)");
        } else {
            $(this).find('.right').css('transform', "rotate(180deg)");
            $(this).find('.left').css('transform', "rotate(" + (num - 180) + "deg)");
        };
    });

});

var DailyRecordApp = {
    total_score: function () {
        $.ajax({
            url: '/get_total_score',
            type: 'GET',
            success: function (data) {
                $('#nav-score').html('<i class="fa fa-line-chart"></i> &nbsp;<b>' + data + '</b>')
            },
        });
    },
    this_month_score: function () {
        $.ajax({
            url: '/get_month_score',
            type: 'GET',
            success: function (data) {
                $('#month-score').html(data)
            },
        });
    },
    prev_month_score: function () {
        $.ajax({
            url: '/get_prev_month_score',
            type: 'GET',
            success: function (data) {
                    $('#prev-month-score').html(data)
            },
        });
    },
    refreshScore: function () {
        this.total_score()
        this.this_month_score()
        this.prev_month_score()
        DailyRecordApp.updateTitle()
    },
    showHabitList: function () {
        // $('#loadingModal').modal('show')
        $.ajax({
            url: '/show_habit_list',
            type: 'GET',
            success: function (data) {
                $('#main_content').html(data)
                $('#loadingModal').modal('hide')
            },
        })
    },
    showHabitCharts: function () {
        $.ajax({
            url: '/show_habit_charts',
            type: 'GET',
            success: function (data) {
                $('#main_content').html(data)
            },
        })
    },

    showMyFormModal: function (url, title) {
        $.ajax({
            url: url,
            type: 'GET',
            success: function (data) {
                $('#myFormModalLabel').html(title)
                $('#myFormModalBody').html(data)
                $('#myFormModal').modal('show')
            }
        })
    },
    updateTitle: () => {
        $.get('/get_done_on_total_today', (data) => {
            document.title = '(' + data.done + '/' + data.total + ') ' + document.title;

        })

    }

}

Date.prototype.Format = function (fmt) { //author: meizz   
    var o = {
        "M+": this.getMonth() + 1, //月份   
        "d+": this.getDate(), //日   
        "h+": this.getHours(), //小时   
        "m+": this.getMinutes(), //分   
        "s+": this.getSeconds(), //秒   
        "q+": Math.floor((this.getMonth() + 3) / 3), //季度   
        "S": this.getMilliseconds() //毫秒   
    };
    if (/(y+)/.test(fmt))
        fmt = fmt.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));
    for (var k in o)
        if (new RegExp("(" + k + ")").test(fmt))
            fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)));
    return fmt;
}