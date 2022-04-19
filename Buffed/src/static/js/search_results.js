$(document).ready(function () {
    $(".save-meal-button").click(function (e) {
        console.log('Button clicked with id ' + this.id);
        e.preventDefault();
        $.ajax({
            type: "POST",
            contentType: 'application/json',
            dataType: 'json',
            url: $(this).hasClass('btn-primary') ? "/find_meals/save_meal/" : "/find_meals/remove_meal/",
            context: this,
            data: JSON.stringify({id: this.id}),
            success: function (result) {
                if ($(this).hasClass('btn-primary')) {
                    $(this).removeClass('btn-primary');
                    $(this).addClass('btn-danger')
                    $(this).text('- Unsave Meal');
                    alert('Added!')
                } else {
                    $(this).removeClass('btn-danger');
                    $(this).addClass('btn-primary');
                    $(this).text('+ Save Meal');
                    alert('Removed!')
                }
            },
            error: function (result) {
                alert('Failed to save meal');
            }
        });
    });
});