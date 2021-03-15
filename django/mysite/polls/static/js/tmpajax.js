$(document).ready(function(){
    
    (function($) {
        "use strict";

    jQuery.validator.addMethod('answercheck', function (value, element) {
        return this.optional(element) || /^\bcat\b$/.test(value)
    }, "type the correct answer");

    // validate contactForm form
    $(function() {
        $('#contactForm').validate({
            rules: {
                name: {
                    required: true,
                    minlength: 2
                }
            },
            messages: {
                name: {
                    required: "내용을 입력해 주세요!",
                    minlength: "이름은 2글자 이상부터 가능합니다"
                }
            },
            submitHandler: function(form) {
                $(form).ajaxSubmit({
                    type:"POST",
                    data: $('#contactForm').serialize(),
                    url:"tmp",
                    beforeSend:function(){
                        console.log("beforesend");
                    },
                    success: function() {
                        console.log("afteresend");
                    },
                    error: function() {
                        console.log("error");
                    }
                })
            }
        })
    })
        
 })(jQuery)
})