jQuery(function() {
    //keep the focus on the input box so that the highlighting
    //I'm using doesn't give away the hidden select box to the user
    $('select.data-list-input').focus(function() {
        $(this).siblings('input.data-list-input').focus();
    });
    //when selecting from the select box, put the value in the input box
    $('select.data-list-input').change(function() {
        $(this).siblings('input.data-list-input').val($(this).val());
    });
});