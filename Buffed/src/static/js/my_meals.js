$(document).ready(function () {

    const successAlert = $("#success-alert");
    const failAlert = $("#fail-alert");

    $(".save-meal-button").click(function (e) {
        e.preventDefault();
        $(this).prop('disabled', true);
        $(this).text('...');
        $.ajax({
            type: "POST",
            contentType: 'application/json',
            dataType: 'json',
            url: $(this).hasClass('btn-success') ? "/find_meals/save_meal/" : "/find_meals/remove_meal/",
            context: this,
            data: JSON.stringify({id: this.id}),
            success: function (result) {
                if ($(this).hasClass('btn-success')) {
                    $(this).removeClass('btn-success');
                    $(this).addClass('btn-danger')
                    $(this).text('- My Meals');
                    $(this).prop('disabled', false);
                } else {
                    $(this).removeClass('btn-danger');
                    $(this).addClass('btn-success');
                    $(this).text('+ My Meals');
                    $(this).prop('disabled', false);
                }
            },
            error: function (result) {
                alert('Failed to save meal');
            }
        });
    });

    $(".todays-plan-button").click(function (e) {
        let mealID = this.id.substring(6);
        $("input[name='mealID']").attr("value", mealID)
    });

    $("#meal-selection-form").submit(function(e) {
        e.preventDefault();
        $.ajax({
            type: "POST",
            data: $("#meal-selection-form").serialize(),
            url: "/my_meals/add_to_plan/",
            success: function (result) {
                successAlert.fadeIn();
            },
            error: function (result) {
                failAlert.fadeIn();
            }
        });
    });

    $('.alert').on('close.bs.alert', function (event) {
        event.preventDefault();
        $(this).fadeOut();
    });
});