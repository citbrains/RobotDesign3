function sendAngles(){
	var httpReq = new XMLHttpRequest();
	httpReq.onreadystatechange = function(){
		if(httpReq.readyState != 4 || httpReq.status != 200)
			return;

		document.getElementById("debug").innerHTML += httpReq.responseText;
		document.getElementById("debug").innerHTML += '<br />';
	}
	//var url = "/ajax/last_articles.cgi?num=" + num;
	var url = "/sendAngles.ajax.py?angles="
	for (i=1;i<=6;i++){
		if(i==4)continue;
		angle = document.getElementById("J" + i).value;
		url += angle + ',';
		document.getElementById("J" + i + "value").value = angle;
	}
	url = url.replace(/,$/,"");
	httpReq.open("GET",url,true);
	httpReq.send(null);
}

function numToSlide(obj){
	target = obj.id.replace(/value/,"");
	document.getElementById(target).value = obj.value;
}
