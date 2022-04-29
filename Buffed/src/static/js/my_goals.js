$(document).ready(function() {

    let clickedIndex = 0;

    $(".edit-button").click(function(e) {
        clickedIndex = $(this).attr("data-loop-index");
    });

    $(".form-range").on("change", function(e, ui) {

        let caloriesRange = $("#goalCalorieInput");
        console.log(caloriesRange.attr("value"));
        let carbsRange = $("#goalCarbInput-" + clickedIndex);
        let proteinRange = $("#goalProteinInput-" + clickedIndex);
        let fatRange = $("#goalFatInput-" + clickedIndex);

        let carbsText = $("#new_carbs-" + clickedIndex);
        let proteinText = $("#new_protein-" + clickedIndex);
        let fatText = $("#new_fat-" + clickedIndex);

        if (this.id.startsWith("goalCarbInput")) {
            proteinRange.attr("max", 50);
            proteinText.text("50");
        } else if (this.id.startsWith("goalProteinInput")) {

        } else if (this.id.startsWith("goalFatInput")) {

        }


    });
});