// ����chatGPT�ӿڵ�URLΪ "/api/chat"
const chatUrl = "/api/chat";

// ��ȡDOMԪ��
const topicList = document.querySelector(".topics-list");
const chatList = document.querySelector(".chat-list");
const newTopicInput = document.querySelector(".new-topic input");
const newTopicBtn = document.querySelector(".new-topic.button");
const messageInput = document.querySelector(".message-input");
const messageBtn = document.querySelector(".message-button");

const topicLink = document.querySelector('.topic-link');
const currentTopicInput = document.querySelector('.current-topic');

const new1topic = document.querySelector('.new1-topic');


let activeTopic = null; // ��ǰѡ�еĻ��⣬Ĭ��Ϊ null

function renderTopic(name) {
  return `
    <li>
      <span class="topic-name">${name}</span>
    </li>
  `;
}

function renderMessage(isBot, message) {
  return `
    <div class="chat ${isBot ? "bot-message" : "user-message"}">
      <img class="avatar" src="${isBot ? "img/bot.png" : "img/user.png"}" />
      <div class="message">${message}</div>
    </div>
  `;
}





messageBtn.addEventListener("click", () => {
	  const message = messageInput.value.trim();
	  const topicname = currentTopicInput.value.trim();
	  
	  messageBtn.disabled=true; 
      messageBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';

	  const body = {
			    message: message,
			    topicname: topicname
			  };
	  if (!message) {
	    return;
	  }
	  fetch( "/chatGPTFull_chat", {
	    method: "POST",
	    headers: {
	      "Content-Type": "application/json",
	    },
	    body: JSON.stringify({ body}),
	  })
	    .then(() => {
	      //refreshTopicList();
	  	  messageBtn.disabled=false; 

	  	location.reload();
		  var chatBox = document.getElementsByClassName("chat")[0];
	  	chatBox.scrollTop = chatBox.scrollHeight;


	    })
	    .catch((err) => console.error(err));
	});



function copyToClipboard(pareantDoc) {
	  var text = pareantDoc.querySelector(".message").textContent;
	  var dummy = document.createElement("textarea");
	  document.body.appendChild(dummy);
	  dummy.value = text;
	  dummy.select();
	  document.execCommand("copy");
	  document.body.removeChild(dummy);
	  //alert("已复制到剪贴板！");
	}


function addTopic(pareantDoc) {
	
	  const topicname = new1topic.value.trim();

    
	$.ajax({
		"type" : 'post',
		"url": '/chatGPTFull_Topicname?topicname=' + topicname+'&edittype=add',
		"success" : function(data) {
		window.location.reload();	
  
		}
		// 查询界面
		//$("#setup-sel").append(opts);
		//alert(($("#addid")));
		});   
	
	 
	}
function delTopic(topicname) {
	
  confirm("请确认是否删除话题！");
	$.ajax({
		"type" : 'post',
		"url": '/chatGPTFull_Topicname?topicname=' + topicname+'&edittype=del',
		"success" : function(data) {
		window.location.reload();	

		}
		// 查询界面
		//$("#setup-sel").append(opts);
		//alert(($("#addid")));
		});   
	
	 
	}


function modifyTopic(parentNode) {
	
	  var fieldValue = parentNode.querySelector(".editable-field");
		topicname=parentNode.querySelector(".editable-field").textContent;

	  var fieldValueText = fieldValue.textContent;
	  
	  fieldValue.innerHTML = '<input type="text" class="editable-field-input" value="' + fieldValueText + '">';

	  var inputField = fieldValue.querySelector(".editable-field-input");
	  inputField.focus();

	oldtopicname=parentNode.querySelector(".old-topic").value.trim();
	 // alert(oldtopicname);

	 inputField.addEventListener("blur", function() {
		    // 防止点击输入框冒泡到父元素触发 a 链接的点击事件
		    event.stopPropagation();
	  	  var newValue = inputField.value;
	  	 alert(newValue);
	  	  alert(fieldValueText);
	  	  if (newValue !== "") {
	  		  if(newValue !==fieldValueText){
	  			  

	  			saveTopicName(newValue,fieldValueText);
	  		    //fieldValue.innerHTML = fieldValue.innerHTML; // 将获取到的新值设置回 fieldValue

	  			
	  		  }
	  		  fieldValue.innerHTML = '<input type="text" class="editable-field-input" value="' + newValue + '">';

	  	  } else {
	  		  
	  		  fieldValue.innerHTML = '<input type="text" class="editable-field-input" value="' + fieldValueText + '">';

	  	    alert("标题不能为空");
	  	  }
	  	 // fieldValue.textContent = fieldValue.innerHTML; // 将获取到的新值设置回 fieldValue
	  	});   
	
	 
	}

function setCurrentTopic(topicname) {
    document.getElementById("current-topic").value = topicname;
}

// 在页面加载完成后，检查后台是否返回 topic name 并赋值给 input 元素
//window.addEventListener('load', () => {
  //const topicNameFromBackend = ''; // 从后台获取 topic name 的代码
  //if (a,b,topicNameFromBackend) {
	//  if topicNameFromBackend{
   // currentTopicInput.value = topicNameFromBackend;}
  //}
//});


window.onload = function() {

	  console.log("加载页面 " );

};

var chatBox = document.getElementsByClassName("chat")[0];
chatBox.scrollTop = chatBox.scrollHeight;


var topics = topicList.getElementsByTagName("li");

for (var i = 0; i < topics.length; i++) {
topics[i].addEventListener("dblclick", function() {
    // 防止点击输入框冒泡到父元素触发 a 链接的点击事件
    event.stopPropagation();
  var fieldValue = this.querySelector(".editable-field");
  var fieldValueText = fieldValue.textContent;
  
  fieldValue.innerHTML = '<input type="text" class="editable-field-input" value="' + fieldValueText + '">';

  var inputField = fieldValue.querySelector(".editable-field-input");
  inputField.focus();

  inputField.addEventListener("blur", function() {
	    // 防止点击输入框冒泡到父元素触发 a 链接的点击事件
	    event.stopPropagation();
  	  var newValue = inputField.value;
  	  if (newValue !== "") {
  		  if(newValue !==fieldValueText){

  			saveTopicName(newValue,fieldValueText);
  		    //fieldValue.innerHTML = fieldValue.innerHTML; // 将获取到的新值设置回 fieldValue

  			
  		  }
  		  fieldValue.innerHTML = '<input type="text" class="editable-field-input" value="' + newValue + '">';

  	  } else {
  		  
  		  fieldValue.innerHTML = '<input type="text" class="editable-field-input" value="' + newValue + '">';

  	    alert("标题不能为空");
  	  }
  	 // fieldValue.textContent = fieldValue.innerHTML; // 将获取到的新值设置回 fieldValue
  	});
  

});
}

	function saveTopicName(newValue,fieldValueText) {
		  if (!newValue) { // 如果 fieldValue 不存在则直接退出函数
			    return;
			  }
		 topicname = newValue;
		oldtopicname=fieldValueText;


	$.ajax({
		"type" : 'post',
		"url": '/chatGPTFull_Topicname?topicname=' + topicname+'&edittype=modify'+'&oldtopicname='+oldtopicname,
		"success" : function(data) {
		window.location.reload();	

		}
		// 查询界面
		//$("#setup-sel").append(opts);
		//alert(($("#addid")));
		});    
		
	  console.log("已保存话题 " + topicName);
	}
	
	$(document).ready(function() {

		  // 获取 awesome-arrow 元素并记录其原始样式
		  var $awesomeArrow = $('.awesome-arrow');
		  var originalClass = $awesomeArrow.attr('class');

		  // 点击箭头切换状态
		  $awesomeArrow.click(function() {
		    if ($('.sidebar').hasClass('sidebar-closed')) {
		      $('.sidebar').removeClass('sidebar-closed');
		      $('.chat').removeClass('chat-maximized');
		      $('.message-send').removeClass('message-send-maximized');
		      $('.message-input').removeClass('message-input-maximized');

		      $(this).html('<i class="fas fa-angle-double-left"></i>');

		      // 切换箭头样式为展开时的样式
		      $awesomeArrow.attr('class', originalClass + ' awesome-arrow-expanded');
		    } else {
		      $('.sidebar').addClass('sidebar-closed');
		      $('.chat').addClass('chat-maximized');
		      $('.message-send').addClass('message-send-maximized');
		      $('.message-input').addClass('message-input-maximized');

		      $(this).html('<i class="fas fa-angle-double-right"></i>');

		      // 切换箭头样式为收起时的样式
		      $awesomeArrow.attr('class', originalClass + ' awesome-arrow-collapsed');
		    }
		  });

		  // 在窗口调整大小时检查侧边栏状态
		  $(window).resize(function() {
		    if (window.innerWidth > 767) {
		      $('.sidebar').removeClass('sidebar-closed');
		      $('.chat').addClass('chat-maximized');
		      $('.message-send').addClass('message-send-maximized');
		      $('.message-input').addClass('message-input-maximized');

		      $(this).html('<i class="fas fa-angle-double-left"></i>');

		      // 切换箭头样式为展开时的样式
		      $awesomeArrow.attr('class', originalClass + ' awesome-arrow-expanded');
		    } else {
		      $('.sidebar').addClass('sidebar-closed');
		      $('.chat').removeClass('chat-maximized');
		      $('.message-send').removeClass('message-send-maximized');
		      $('.message-input').removeClass('message-input-maximized');

		      $(this).html('<i class="fas fa-angle-double-right"></i>');

		      // 切换箭头样式为收起时的样式
		      $awesomeArrow.attr('class', originalClass + ' awesome-arrow-collapsed');
		    }
		  });

		  // 初始化窗口状态
		  if (window.innerWidth <= 767) {
		    $('.sidebar').addClass('sidebar-closed');
		    $('.chat').removeClass('chat-maximized');
		    $('.message-send').removeClass('message-send-maximized');
		      $('.message-input').removeClass('message-input-maximized ');

		    $(this).html('<i class="fas fa-angle-double-right"></i>');

		    // 设置箭头样式为收起时的样式
		    $awesomeArrow.attr('class', originalClass + ' awesome-arrow-collapsed');
		  }
		});