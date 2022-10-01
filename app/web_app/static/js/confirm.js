function confirm_menu_01(url){

	if(window.confirm('チョコストロベリーホイップの注文を確定しますか？')){
		location.href = url;
	}
}

function confirm_menu_02(url){

	if(window.confirm('キャラメルフレークホイップの注文を確定しますか？')){
		location.href = url; 
	}
}

function confirm_menu_03(url){

	if(window.confirm('アーモンドチョコホイップの注文を確定しますか？')){
		location.href = url; 
	}
}

function confirm_menu_04(){

	if(window.confirm('バナナチョコホイップの注文を確定しますか？')){
		location.href = "/whip_choco_banana"; 
	}
}

function confirm_menu_05(){

	if(window.confirm('ココアストロベリーカスタードの注文を確定しますか？')){
		location.href = "/custard_strawberry_biscuits"; 
	}
}

function confirm_original_menu(url){

	if(window.confirm('上記の内容で注文を確定しますか？')){
		location.href = url;
	}
}