/**
 * Created by msg on 11/11/16.
 */

$(function(){
    $("#li_member").addClass("active open");
    $("#li_add_member").addClass("active open");
    $("#btn_save").click(function() {
        var validate_result = data_validate("div_member_info");
        if (validate_result[0] == false) {
            show_msg(validate_result[1]);
            return false;
        }
        return true;
    });
});


$(document).ready(function(){
	Bind_Date($(".date"), "left", 1);
});

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
