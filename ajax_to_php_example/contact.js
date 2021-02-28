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
                },
                subject: {
                    required: true,
                    minlength: 4
                },
                number: {
                    required: true,
                    minlength: 5
                },
                email: {
                    required: true,
                    email: true
                },
                message: {
                    required: true,
                    minlength: 20
                }
            },
            messages: {
                name: {
                    required: "내용을 입력해 주세요!",
                    minlength: "이름은 2글자 이상부터 가능합니다"
                },
                subject: {
                    required: "주제는 필요합니다!",
                    minlength: "최소 4글자는 입력해 주세요"
                },
                number: {
                    required: "이 칸은 필수항목입니다!",
                    minlength: "5글자 이상은 필수입니다!"
                },
                email: {
                    required: "이메일은 필수인데요..?"
                },
                message: {
                    required: "정말 보낼 내용이 없으세요? 필수입니다!",
                    minlength: "흠... 더 적을 내용이 없으신가요?"
                }
            },
            submitHandler: function(form) {
                $(form).ajaxSubmit({
                    type:"POST",
                    data: $('#contactForm').serialize(),
                    url:"contact_process.php",
                    beforeSend:function(){
                        $('#sending').show();
                    },
                    success: function() {
                        $('#contactForm :input').attr('disabled', 'disabled');
                        $('#contactForm').fadeTo( "slow", 1, function() {
                            $(form).find(':input').attr('disabled', 'disabled');
                            $(form).find('label').css('cursor','default');
                            $('#success').fadeIn();
                            $('.modal').modal('hide');
                            $('#success').modal('show');
                            $('#sending').hide();
                        })
                    },
                    error: function() {
                        $('#contactForm').fadeTo( "slow", 1, function() {
                            $('#error').fadeIn();
                            $('.modal').modal('hide');
                            $('#error').modal('show');
                            $('#sending').hide();
                        })
                    }
                })
            }
        })
    })
        
 })(jQuery)
})