#!/bin/sh

if [ $# -gt 2 ]
then
	arg1=$1
	arg2=$2
	# arg3=$3

	# export arg3=${ToUserName:-'QACHECK_qab08ab3638b88'}
	# export arg5=${CreateTime:-date}
	
	arg6=""
	for((i=3;i<=$#;i++));do 
		# echo $i
	    eval j=\$$i
	    arg6="${arg6} $j "
	done
	
	echo $arg1,$arg2,$arg6

	python main_manual.py $arg1 $arg2 $arg6
	<<EOF

EOF
else
  	echo '支持类型及输入参数顺序如下，请检查您的数据是否正确!\n事件类型（MsgType）：-t (文本消息) -i (图片消息) -vo（语音消息）-vi (视频消息) -sv (小视频消息) -lo（地理位置消息） -li（链接消息) -e（事件消息)' 			
  	echo '普通文本消息 :   appid, MsgType, Content'
  	echo '图片消息 :   appid, MsgType, MediaId,PicUrl'
  	echo '语音消息 :  tappid, MsgType, MediaId,Format'
  	echo '视频\小视频消息 :  appid, MsgType, MediaId,ThumbMediaId'
  	echo '地理位置消息 :  appid, MsgType, Location_X,Location_Y,Scale,Label'
  	echo '链接消息 :   appid, MsgType, Title,Description,Url'
    echo '关注或取关事件 :  appid, MsgType, Event'
    echo '已关注(subscribe/SCAN) : appid, MsgType, Event, EventKey, TICKET'
    echo '上报地理位置(LOCATION) : appid, MsgType, Event, Latitude, Longitude, Precision'
    echo '自定义菜单(CLICK／VIEW) : appid, MsgType, Event, EventKey, TICKET'
    echo '示例：sh push.sh wx15426e0b8f518593 -t 测试文本消息'
fi	
