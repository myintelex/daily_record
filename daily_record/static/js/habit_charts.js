var habitcharts = {
    showHistoryChart: function (category) {
        $.get('/get_categorys_name', data => habitcharts.initHistoryChart(data))
    },
    initHistoryChart: function (categorys) {
        var myChart = echarts.init(document.getElementById('history-chart'));
        var series = categorys.map(item => {
            return {
                name: item,
                type: 'scatter',
                encode: {
                    x: 'date',
                    y: item
                }
            }
        })
        series.push({
            name: 'Total',
            type: 'line',
            symbol: 'circle',
            smooth: true,
            encode: {
                x: 'date',
                y: 'value'
            },
            markPoint: {
                data: [{
                    type: 'max',
                    name: '最大值'
                }, {
                    type: 'min',
                    name: '最小值'
                }]
            },
            markLine: {
                data: [{
                    type: 'average',
                    name: '平均值'
                }]
            }
        })
        var option = {
            dataZoom: [{
                type: 'slider',
                filterMode: 'filter',
                start: 90,
                end: 100
            }],
            legend: {
                selector: ['all', 'inverse']
            },
            tooltip: {
                trigger: 'axis',
                axisPointer: {
                    type: 'shadow'
                }
            },
            toolbox: {
                feature: {
                    myTool1: {
                        show: true,
                        title: '展示得分数据',
                        icon: 'path://M60 50 a40 40 0 1 0 80 0 a40 40 0 1 0 -80 0 z',
                        onclick: function () {
                            myChart.showLoading()
                            habitcharts.getHistoryData(myChart, 'Value')
                        }
                    },
                    myTool2: {
                        show: true,
                        title: '展示完成数量数据',
                        icon: 'path://M60 50 a40 40 0 1 0 80 0 a40 40 0 1 0 -80 0 z',
                        onclick: function () {
                            myChart.showLoading()
                            habitcharts.getHistoryData(myChart, 'cnt')
                        }
                    }
                }
            },
            xAxis: {
                type: 'category',
                splitLine: {
                    show: true,
                },
            },
            yAxis: {},
            series: series,
        }
        myChart.setOption(option)
        myChart.showLoading()

        this.getHistoryData(myChart, 'Value')
    },

    getHistoryData: function (myChart, type) {
        $.get('get_history_data', {
            type: type
        }, data => {
            myChart.hideLoading()
            myChart.setOption({ //加载数据图表
                dataset: {
                    source: data.data
                },
            });
        })
    },


    get_category_data: function (chart) {
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
                            series: {
                                id: 'pie2',
                                data: cate[0].habits

                            }
                        })

                    }

                });
            }
        })
    },

    show_category_chart: function () {
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
        }; // 使用刚指定的配置项和数据显示图表。 myChart.setOption(option);
    },

    show_calendar_chart: function () {
        var myChart = echarts.init(document.getElementById('calendar-chart'));
        var days = Array.from({
            length: 31
        }, (v, k) => k);
        var cate = Array.from('abcdefgh')

        var data = days.map(function (item) {
            return [item, 2, Math.floor(Math.random() * 10) + 1]
        })
        console.log(data)

        for (var i = 0; i < 8; i++) {
            data = data.concat(days.map(function (item) {
                return [item, i, Math.floor(Math.random() * 10) + 1]
            }))

        }
        console.log(data)
        var option = {
            animation: false,
            grid: {
                top: 0,
                height: '90%',
            },
            xAxis: {
                type: 'category',
                data: days,
                axisLine: {
                    show: false
                },
                axisTick: {
                    show: false
                },
                splitLine: {
                    show: true
                },
                splitArea: {
                    show: true
                }
            },
            yAxis: {
                type: 'category',
                data: cate,
                splitLine: {
                    show: true
                },
                axisLine: {
                    show: false
                },
                axisTick: {
                    show: false
                },
                splitArea: {
                    show: true
                }
            },
            visualMap: {
                min: 0,
                max: 10,
                calculable: true,
                orient: 'horizontal',
                left: 'center',
                bottom: '15%',
                show: false
            },
            series: [{
                name: 'Punch Card',
                type: 'heatmap',
                data: data,
                itemStyle: {
                    color: {
                        type: 'linear',
                        x: 0,
                        y: 0,
                        x2: 0,
                        y2: 1,
                        colorStops: [{
                            offset: 0,
                            color: 'gray' // 0% 处的颜色
                        }, {
                            offset: 1,
                            color: 'blue' // 100% 处的颜色
                        }],
                        global: false // 缺省为 false
                    },
                    borderColor: '#000'
                },
            }]
        };
        myChart.setOption(option)
    },
    showCategoryChart: () => {
        var myChart = echarts.init(document.getElementById('category-chart'));
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
            }, {
                name: 'habits',
                type: 'pie',
                radius: [30, 110],
                center: ['75%', '50%'],
                id: 'pie2',
                data: []
            }]
        }; // 使用刚指定的配置项和数据显示图表。 
        myChart.setOption(option);
        habitcharts.getCategoryData(myChart)
    },
    getCategoryData: (chart) => {
        $.get('get_category_data', (data) => {
            chart.setOption({
                series: {
                    id: 'pie1',
                    data: data
                }
            })
            chart.on('click', {
                seriesId: 'pie1'
            }, (params) => {
                cate = data.filter(category => category.name === params.name)
                if (cate) {
                    chart.setOption({
                        series: {
                            id: 'pie2',
                            data: cate[0].habits
                        }
                    })
                }
            });
        })
    },
}


$(document).ready(function () {
    habitcharts.showHistoryChart()
    habitcharts.showCategoryChart()
})