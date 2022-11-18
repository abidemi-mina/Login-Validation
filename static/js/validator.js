
// just for the demos, avoids form submit
jQuery.validator.setDefaults({
    debug: true,
    success:  function(label){
        label.attr('id', 'valid');
    },
});
$( "#myform" ).validate({
    rules: {
        password: "required",
        confirm_password: {
            equalTo: "#password"
        }
    },
    messages: {
        full_name: {
            required: "Please provide an username"
        },
        your_email: {
            required: "Please provide an email"
        },
        password: {
            required: "Please provide a password"
        },
        confirm_password: {
            required: "Please provide a password",
            equalTo: "Wrong Password"
        }
    }
});
