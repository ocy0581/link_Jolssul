<?php
	use PHPMailer\PHPMailer\PHPMailer;
	use PHPMailer\PHPMailer\Exception;
	
	require './assets/PHPMailer-master/vendor/autoload.php';

    $to = "syu9710@gmail.com";
	$from = $_REQUEST['email'];
    $name = $_REQUEST['name'];
    $subject = $_REQUEST['subject'];
    //$number = $_REQUEST['number'];
	$cmessage = $_REQUEST['message'];
	
	$mail = new PHPMailer(true);
	/*
	$from = "syu9710@gmail.com";
	$name = "유승범";
	$subject = "test mailing";
	$cmessage = "test message";
	*/


	try{
		//서버 세팅
		$mail->SMTPDebug = 2;
		$mail->isSMTP(); //SMTP 사용 설정
		$mail->Host = "smtp.gmail.com";
		$mail->SMTPAuth=true;
		//google 한정 보안 정책 변경으로 ssl이 아니라 tls로 해야함!!!!
		//참고 스택오버플로우
		$mail->SMTPSecure = "tls";
		$mail->SMPTAutoTLS = false;
		$mail->Username = "syu9710@gmail.com";
		//비밀번호는 제출시에 가렸습니다
		$mail->Password = "비밀번호는 가렸습니다. 영상 참고 부탁드립니다.";
		$mail->Port = 587;

		$mail->CharSet="utf-8";
		//메일 전송자
		$mail->setFrom($from,$name);
		//받는 메일
		$mail->addAddress("syu9710@gmail.com","ysb");
		$mail->isHTML(true);
		$mail->Subject = $subject;
		$mail->Body = $cmessage;
		//Gmail CA인증체크 해지
		$mail -> SMTPOptions = array(
			"ssl" => array(
			"verify_peer" => false
			, "verify_peer_name" => false
			, "allow_self_signed" => true
			)
		);
		$result = $mail->send();
		
		if($result){
			echo "success";
		}
		else {
			echo "error";
		}

	}catch (phpmailerException $e) {
		echo $e->errorMessage();
	} catch (Exception $e) {
		echo $e->getMessage();
	}
	
?>