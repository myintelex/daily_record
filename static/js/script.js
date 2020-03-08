$(document).ready(function () {
    $('[data-toggle="tooltip"]').tooltip()
    $(document).on('click', '.habit-item', function () {
        id = $(this).attr('hab_id')
        var $this = $(this);
        $.ajax({
            url: '/change_habit_state/' + id,
            type: 'POST',
            complete: function () {
                $('#btn-habit-list').click()
            },
            success: function (data) {},
            error: function (data) {
                toastr.error(data.status + ' ' + data.statusText)
            }
        });
    })
    $(document).on('click', '#btn-habit-list', function () {
        $.ajax({
            type: 'GET',
            url: 'habit_list',
            success: function (data) {
                $('#main_content').html(data.html)
                $('#nav-score').html('<i class="fa fa-line-chart"></i><b>' + data.record + '</b>')
            }
        })
    })

    function get_history_data(myChart, type) {
        var series = []
        for (var i = 0; i < 8; i++) {
            if (type == 'value') {
                series.push({
                    type: 'bar',
                    stack: i
                })
            } else {
                series.push({
                    type: 'bar',
                    stack: 'cnt'
                })
            }
        }
        series.push({
            type: 'line',
            smooth: true,
            itemStyle: {
                color: 'red'
            },
            markPoint: {
                data: [{
                        type: 'max',
                        name: '最大值'
                    },
                    {
                        type: 'min',
                        name: '最小值'
                    }
                ]
            },
            markLine: {
                data: [{
                    type: 'average',
                    name: '平均值'
                }]
            }
        })
        $.ajax({
            type: 'GET',
            url: 'get_history_data',
            data: {
                type: type
            },
            success: function (data) {
                console.log(data)
                myChart.hideLoading()
                myChart.setOption({ //加载数据图表
                    dataset: {
                        source: data
                    },
                    series: series,
                });
            }
        })
    }

    function show_history_chart(category) {
        var myChart = echarts.init(document.getElementById('history-chart'));
        var selected = {}
        console.log(selected)
        myChart.setOption({
            toolbox: {
                feature: {
                    myTool1: {
                        show: true,
                        title: '展示得分数据',
                        icon: 'path://M60 50 a40 40 0 1 0 80 0 a40 40 0 1 0 -80 0 z',
                        onclick: function () {
                            myChart.showLoading()
                            get_history_data(myChart, 'value')
                        }
                    },
                    myTool2: {
                        show: true,
                        title: '展示完成数量数据',
                        icon: 'path://M60 50 a40 40 0 1 0 80 0 a40 40 0 1 0 -80 0 z',
                        onclick: function () {
                            myChart.showLoading()
                            get_history_data(myChart, 'cnt')
                        }
                    }
                }
            },
            dataZoom: [{
                type: 'inside'
            }],
            tooltip: {
                trigger: 'axis',
                axisPointer: {
                    type: 'shadow'
                }
            },
            legend: {
                selected: selected
            },
            dataset: {
                dimensions: ['date'].concat(category).concat('value'),
                source: []
            },
            xAxis: {
                type: 'category'
            },
            yAxis: {},
            series: [{
                type: 'bar'
            }],
        })
        myChart.showLoading()

        get_history_data(myChart, 'value')
    }

    function get_category_data(chart) {
        $.ajax({
            type: 'GET',
            url: 'get_category_data',
            success: function (data) {
                console.log(data)
                chart.setOption({
                    series: {
                        id: 'pie1',
                        data: data
                    }

                })
                chart.on('click', {
                    seriesId: 'pie1'
                }, function (params) {
                    cate = data.filter(category => category.name === params.name)
                    if (cate) {
                        chart.setOption({
                            series :{
                                id: 'pie2',
                                data:cate[0].habits

                            }
                        })

                    }

                });
            }
        })
    }

    function show_category_chart() {
        var myChart = echarts.init(document.getElementById('category-chart'));
        get_category_data(myChart)
        var option = {
            tooltip: {
                trigger: 'item',
                formatter: '{a} <br/>{b} : {c} ({d}%)'
            },
            legend: {
                left: 'center',
                top: 'bottom',
            },
            series: [{
                    name: 'Categorys ',
                    type: 'pie',
                    selectedMode: true,
                    radius: [30, 110],
                    center: ['25%', '50%'],
                    roseType: 'area',
                    id: 'pie1',
                    data: []
                },
                {
                    name: 'habits',
                    type: 'pie',
                    radius: [30, 110],
                    center: ['75%', '50%'],
                    id: 'pie2',
                    data: []
                }
            ]
        };

        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);
    }


    $(document).on('click', '#btn-charts', function () {
        $.ajax({
            type: 'GET',
            url: 'charts',
            success: function (data) {
                $('#main_content').html(data.html)
                show_history_chart(data.categorys)
                show_category_chart()
            }
        })
    })
    $('#btn-charts').click()




});


function show_new_habit_modal() {
    $.ajax({
        url: '/new_habit', // 目标URL
        type: 'GET', // 请求方法
        success: function (data) { // 返回2XX响应后触发的回调函数
            console.log('success')
            $('#myModalBody').html(data)
            $('#myModal').modal('show')
            console.log('xxx')
        }
    })
}

function item_click(a) {
    $.ajax({
        type: 'GET',
        url: $(a).attr('url'),
        success: function (data) {
            if (data.html) {
                $('#main_content').html(data.html)
                show_habit_chart()
            } else {
                console.log($('#habit_chart_15').attr('id'))
                $('#main_content').html(data)
            }
        }
    })
}

function del_habit(id) {
    $.ajax({
        url: '/del_habit/' + id, // 目标URL
        type: 'POST', // 请求方法
        complete: function () {
            $('#btn-habit-list').click()
        },
        success: function (data) {
            toastr.info(data.message)
        },
        error: function (data) {
            toastr.error(data.responseJSON.message, data.status + ' ' + data.statusText)
        }
    })
}

function change_habit_state(id) {
    $.ajax({
        url: '/change_habit_state/' + id, // 目标URL
        type: 'POST', // 请求方法
        complete: function () {
            $('#btn-habit-list').click()
        },
        success: function (data) {
            if (data.state) {

            }
        },
        error: function (data) {
            toastr.error(data.status + ' ' + data.statusText)
        }
    })
}

function show_edit_habit_modal(id) {
    $.ajax({
        url: '/edit_habit/' + id, // 目标URL
        type: 'GET', // 请求方法
        success: function (data) { // 返回2XX响应后触发的回调函数
            console.log('success')
            $('#myModalBody').html(data)
            $('#myModal').modal('show')
            console.log('xxx')
        }
    })
}