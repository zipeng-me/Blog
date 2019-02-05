/**
 * Created by tarena on 18-11-6.
 */
function getXhr(){
    //如果浏览器支持XMLHttpRequest,则创建XMLHttpRequest的对象并返回
    if(window.XMLHttpRequest){
        return new XMLHttpRequest();
    }else{
        //如果浏览器不支持XMLHttpRequest的话,则创建ActiveXObject的对象并返回
        return new ActiveXObject("Microsoft.XMLHTTP");
    }
}