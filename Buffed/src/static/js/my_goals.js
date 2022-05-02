$(document).ready(function() {

    let clickedIndex = 0;

    $(".edit-button").click(function(e) {
        clickedIndex = $(this).attr("data-loop-index");
        console.log(clickedIndex);
    });
    $("#editGoalForm-" + clickedIndex).validate({
        errorClass: "error fail-alert",
        validClass: "valid success-alert",
        rules: {
            goal_id: {
                required: true,
            },
            goal_name: {
                required: true,
                minlength: 1,
                maxlength: 50,
            },
            calories: {
                required: true,
                number: true,
                min: 1000,
                max: 10000,
            },
            number_of_meals: {
                required: true,
                number: true,
                min: 1,
                max: 25,
            },
            desired_weight: {
                required: true,
                number: true,
                min: 25,
                max: 2000
            },
        },
        messages: {
            goal_name: {
                required: "You must enter a goal name",
                minlength: "Goal name must be at least one character",
                maxlength: "Goal name must be no longer than 50 characters"
            },
            calories: {
                required: "Calorie amount is required",
                number: "Calorie amount must be numeric",
                min: "Minimum calorie amount is 1000",
                max: "Maximum calorie amount is 10000"
            },
            number_of_meals: {
                required: "You must enter a number of meals",
                number: "Number of meals must be numeric",
                min: "Minimum amount of meals is 1",
                max: "Maximum amount of meals is 25"
            },
            desired_weight: {
                required: "You must enter a desired weight",
                number: "Desired weight must be numeric",
                min: "Minimum weight required is 25 lbs",
                max: "Maximum weight required is 2000 lbs"
            },
        },

    });
    $('#').click(function(event) {
        event.preventDefault();
        $.post(url, data=$('#editForm').serialize(), function(data) {
            if (data.status == 'ok') {
                $("#editGoalForm-" + clickedIndex).modal('hide');
                location.reload();
            }
    else {
      $('#editModal .modal-content').html(data);
    }
  });
})
});
