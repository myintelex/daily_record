var habitList = {
    showNewHabitForm: function () {
        DailyRecordApp.showMyFormModal('/new_habit', 'New Habit')
    },
    showEditHabitForm: function (id) {
        DailyRecordApp.showMyFormModal('/edit_habit/' + id, 'Edit Habit')
    },
    delHabit: function (id) {
        DailyRecordApp.showMyFormModal('/del_habit/' + id, 'Edit Habit')
    },

    changeHabitState: function (id, date, func) {
        $.ajax({
            url: '/change_habit_state/' + id,
            type: 'GET',
            data: {
                date: date
            },
            success: function (data) {
                habitList.changeCategoryDoneCnt(data.category_name)
                DailyRecordApp.refreshScore()
                $('#habit-' + id + '-total-done').html(data.total_cnt)
                $('#habit-' + id + '-continue-done').html(data.continue_cnt)
                $('#habit-' + id + '-progress').css("width", data.habit_progress.progress + "%")
                $('#habit-' + id + '-progress').css("width", data.habit_progress.progress + "%")
                if (data.state) {
                    $('#habit-' + date + '-' + id).removeClass("bg-light");
                    $('#habit-' + date + '-' + id).addClass("bg-success");
                } else {
                    $('#habit-' + date + '-' + id).removeClass("bg-success");
                    $('#habit-' + date + '-' + id).addClass("bg-light");
                }
                console.log(date)
                console.log(new Date().Format('yyyy-MM-dd'))
                console.log(date == new Date().Format('yyyy-MM-dd'))
                if (date == new Date().Format('yyyy-MM-dd')) {
                    if (data.state) {
                        $('#habit-' + id + '-name').addClass("text-secondary");
                        $('#habit-' + id + '-name').removeClass("text-body");
                        $('#habit-' + id + '-name').html("<i class='fa fa-check-square-o' ></i> " + data.habit_name)
                    } else {
                        $('#habit-' + id + '-name').removeClass("text-secondary");
                        $('#habit-' + id + '-name').addClass("text-body");
                        $('#habit-' + id + '-name').html("<i class='fa fa-square-o' ></i> " + data.habit_name)
                    }
                }
            },
            error: function (data) {
                toastr.error(data.status + ' ' + data.statusText)
            }
        });
    },
    changeCategoryDoneCnt: function (categoryName) {
        console.log('cate')
        $.ajax({
            url: '/get_category_done_cnt/' + categoryName,
            type: 'GET',
            success: function (data) {
                console.log(data)
                $('#' + categoryName + '_done_cnt').html(data.done_cnt + "/" + data.total_cnt)
            },
            error: function (data) {
                toastr.error(data.status + ' ' + data.statusText)
            }
        });
    },

}
$(document).ready(function () {
    $(document).off('click', '.habit-item')
    $(document).on('click', '.habit-item', function () {
        id = $(this).attr('hab-id')
        var now = new Date()
        habitList.changeHabitState(id, now.Format('yyyy-MM-dd'))
    })
    $(document).off('click', '.habit-calendar-btn')
    $(document).on('click', '.habit-calendar-btn', function () {
        console.log("click")
        id = $(this).attr('habit-id')
        date = $(this).attr('date')
        habitList.changeHabitState(id, date)
    })
    $(document).on('click', '#simplyDisplaySwitch', function () {
        console.log('sd')
        if ($(this).prop("checked")) {
            $('.category-name').css('display', 'none');
            $('.habit-small').css('display', 'none');
            $('.habit-thisweek').css('display', 'none');
            $('.habit-progress').css('display', 'none');
        }else {
            $('.category-name').css('display', 'block');
            $('.habit-small').css('display', 'block');
            $('.habit-thisweek').css('display', 'block');
            $('.habit-progress').css('display', 'flex');

        }

    })
})