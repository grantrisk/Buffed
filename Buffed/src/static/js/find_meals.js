$(document).ready(function() {

    const dietsRow = $("#dietsRow");
    const rangesRow = $("#rangesRow");

    const minCalories = $("#minCalories");
    const maxCalories = $("#maxCalories");
    const minCarbs = $("#minCarbs");
    const maxCarbs = $("#maxCarbs");
    const minFat = $("#minFat");
    const maxFat = $("#maxFat");

    $("#matchUserDiet").change(function() {
        if ($(this).prop('checked')) {
            dietsRow.fadeOut();
        } else {
            dietsRow.fadeIn();
        }
    });

    $("#matchUserGoal").change(function() {
        if ($(this).prop('checked')) {
            rangesRow.fadeOut();
        } else {
            rangesRow.fadeIn();
        }
    });
});