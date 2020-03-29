$(document).ready(function () {
    $('#nav-score').html('<i class="fa fa-line-chart"></i> &nbsp;<b><i class="fa fa-refresh fa-spin"></i> </i></b>')
    $('#month-score').html('<i class="fa fa-ellipsis-h"></i>')
    $('#prev-month-score').html('<i class="fa fa-ellipsis-h "></i>')

    DailyRecordApp.refreshScore()
    DailyRecordApp.showHabitList()
    DailyRecordApp.showHabitLinks()
    DailyRecordApp.showCalendarChart()
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

    },
    showCalendarChart: () => {
        function getVirtulData(year) {
            year = year || '2017';
            var date = +echarts.number.parseDate(year + '-01-01');
            var end = +echarts.number.parseDate((+year + 1) + '-01-01');
            var dayTime = 3600 * 24 * 1000;
            var data = [];
            for (var time = date; time < end; time += dayTime) {
                data.push([
                    echarts.format.formatTime('yyyy-MM-dd', time),
                    Math.floor(Math.random() * 10000)
                ]);
            }
            return data;
        }
        var myChart = echarts.init(document.getElementById('calendar-chart'));

        var option = {
            tooltip: {},
            visualMap: {
                min: 0,
                max: 10000,
                type: 'piecewise',
                orient: 'horizontal',
                left: 'center',
                top: 0,
                textStyle: {
                    color: '#000'
                }
            },
            calendar: {
                top: 50,
                left: 30,
                right: 30,
                cellSize: ['auto', 13],
                range: '2016',
                itemStyle: {
                    borderWidth: 0.5
                },
                yearLabel: {
                    show: false
                }
            },
            series: {
                type: 'heatmap',
                coordinateSystem: 'calendar',
                data: getVirtulData(2016)
            }
        };
        myChart.setOption(option);
    },
    showHabitLinks: () => {
        $.get('/get_categorys_name', data => {
            console.log(data)
            data.forEach(element => {
                console.log(element)
                $('#CategoryLinks').append(' <li class="nav-item">' +
                    ' <a class="nav-link" href="#">' + element + '</a> </li>')
            });


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