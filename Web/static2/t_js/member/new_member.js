/**
 * Created by msg on 11/11/16.
 */

$(function(){
    $("#li_member").addClass("active open");
    $("#btn_save").click(function() {
        var validate_result = data_validate("div_member_info");
        if (validate_result[0] == false) {
            show_msg(validate_result[1]);
            return false;
        }
        return true;
    });
});
/*首页数字跳动*/
/*!
 * chaffle v1.0.0
 * Licensed under MIT
 * Copyright 2013-2014 blivesta
 * http://blivesta.com
 */
(function($){var namespace="chaffle";var methods={init:function(options){options=$.extend({speed:20,time:140},options);return this.each(function(){var _this=this;var $this=$(this);var data=$this.data(namespace);if(!data){options=$.extend({},options);$this.data(namespace,{options:options})}var $text=$this.text();var substitution;var shuffle_timer;var shuffle_timer_delay;var shuffle=function(){$this.text(substitution);if($text.length-substitution.length>0){for(i=0;i<$text.length-substitution.length;i++){var shuffleStr=random_text.call();$this.append(shuffleStr)}}else{clearInterval(shuffle_timer)}};var shuffle_delay=function(){if(substitution.length<$text.length){substitution=$text.substr(0,substitution.length+1)}else{clearInterval(shuffle_timer_delay)}};var random_text=function(){var str;var lang=$this.data("lang");switch(lang){case"en":str=String.fromCharCode(33+Math.round(Math.random()*99));break;case"zh":str=String.fromCharCode(19968+Math.round(Math.random()*80));break;case"ja-hiragana":str=String.fromCharCode(12352+Math.round(Math.random()*50));break;case"ja-katakana":str=String.fromCharCode(12448+Math.round(Math.random()*84));break}return str};var start=function(){substitution="";clearInterval(shuffle_timer);clearInterval(shuffle_timer_delay);shuffle_timer=setInterval(function(){shuffle.call(_this)},options.speed);shuffle_timer_delay=setInterval(function(){shuffle_delay.call(this)},options.time)};$this.unbind("mouseover."+namespace).bind("mouseover."+namespace,function(){start.call(_this)})})},destroy:function(){return this.each(function(){var $this=$(this);$(window).unbind("."+namespace);$this.removeData(namespace)})}};$.fn.chaffle=function(method){if(methods[method]){return methods[method].apply(this,Array.prototype.slice.call(arguments,1))}else if(typeof method==="object"||!method){return methods.init.apply(this,arguments)}else{$.error("Method "+method+" does not exist on jQuery."+namespace)}}})(jQuery);
//首页数字跳动
$(document).ready(function() {
    $('.chaffle').chaffle({
      speed: 10,
      time: 60
    });
  });
//end

var dt = null;
/**
 * Unicorn Admin Template
 * Diablo9983 -> diablo9983@gmail.com
**/
$(document).ready(function(){
	//==================预约日期+时间===================//
	$('#reservationtime').daterangepicker({
											startDate: moment(),
											singleDatePicker: true,
											showDropdowns: true,
											timePicker: true,
											timePickerIncrement:5,
											format: 'YYYY-DD-MM A h:mm'
										});

	Bind_Date($(".date"), "left", 1);
	//Bind_Date($("#opencardday"));
	Bind_Date($("#joiningdate"));
	Bind_Date($('.selectdate'), "right", 2);
	Bind_Date($('.selectdate-left'), "left", 2);
});
function reloadpage(){
	var href = window.location.href;
	var str = href.substr(href.length-1,1)
	if(str == '#'){
		href = href.substr(0,href.length-1);
	}
	href = changeURLPar(href, 'pagesize', dt.page.len());
	href = changeURLPar(href, 'page', dt.page());
	window.location.href=href;
}
//绑定时间控件
//opens: right | left
//isone: 2:双日历， 其他单个日历（默认）
function Bind_Date(obj, opens, isone){
	//双控件
	if (isone==2)
	{
		var DateOpetion = {
			startDate: moment().subtract('days', 0),
			endDate: moment(),
			opens: opens,
			ranges: {
				'今天': [moment(), moment()],
				'昨天': [moment().subtract('days', 1), moment().subtract('days', 1)],
				'最近7天': [moment().subtract('days', 6), moment()],
				'最近30天': [moment().subtract('days', 29), moment()],
				'这个月': [moment().startOf('month'), moment().endOf('month')],
				'上个月': [moment().subtract('month', 1).startOf('month'), moment().subtract('month', 1).endOf('month')]
			}
		};

		obj.daterangepicker(DateOpetion).on('apply.daterangepicker', function(ev, picker) {
			$(this).find('span').html(picker.startDate.format('YYYY-MM-DD') + ' - ' + picker.endDate.format('YYYY-MM-DD'));
		});
	}else{
		//单控件
		obj.daterangepicker({
			startDate: moment(),
			singleDatePicker: true,
			showDropdowns: true,
			opens: opens,
			format:'YYYY-MM-DD'
		});
	}
}
