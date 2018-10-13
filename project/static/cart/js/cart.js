$(document).ready(function () {
    var subShoppings = document.getElementsByClassName("subShopping")
    var addShoppings = document.getElementsByClassName("addShopping")

     // 减少商品数量
    for(var i = 0; i < subShoppings.length; i++){
        subShopping = subShoppings[i]
        subShopping.addEventListener("click", function () {
            pid = this.getAttribute("ga")
            $.post('/changecart/1/', {"productid": pid}, function (data) {
                if(data.status == "success") {
                    //添加成功，把中间的span的innerHTML变成当前的数量
                    document.getElementById(pid).innerHTML = data.data
                    document.getElementById(pid + "price").innerHTML = data.price
                    document.getElementById("sumprice").innerHTML = data.sumprice
                    if(data.data == 0){
                        var li = document.getElementById(pid + "li")
                        li.parentNode.removeChild(li)
                    }
                }
            })
        })
    }

     // 增加商品数量
    for(var i = 0; i < addShoppings.length; i++){
        addShopping = addShoppings[i]
        addShopping.addEventListener("click", function () {
            pid = this.getAttribute("ga")
            $.post('/changecart/0/', {"productid": pid}, function (data) {
                if(data.status == "success") {
                    //添加成功，把中间的span的innerHTML变成当前的数量
                    document.getElementById(pid).innerHTML = data.data
                    document.getElementById(pid + "price").innerHTML = data.price
                    document.getElementById("sumprice").innerHTML = data.sumprice
                }
            })
        })
    }

     // 勾选即将下订单的商品
    var ischoses = document.getElementsByClassName("ischose")
    for (var i = 0; i < ischoses.length; i++){
        ischose = ischoses[i]
        ischose.addEventListener("click", function () {
            pid = this.getAttribute("goodsid")
            $.post('/changecart/2/', {"productid": pid}, function (data) {
                if (data.status == "success") {
                    document.getElementById(pid + "a").innerHTML = data.data
                    document.getElementById("sumprice").innerHTML = data.sumprice
                }
            })
        })
    }

     // 全部选择
    var selectall = document.getElementById("selectall")
    selectall.addEventListener("click", function () {
        $.post('/changecart/3/', function (data) {
            if (data.status == "success") {
                document.getElementById("sumprice").innerHTML = data.sumprice
                document.getElementById("str1").innerHTML = data.str
            }
        })
    })

     // 确认下单
    var ok = document.getElementById("ok")
    ok.addEventListener("click", function () {
        var f = confirm("是否确认下单？")
        if (f) {
            $.post('/saveorder/', function (data) {
                if (data.status == "success") {
                    window.location.href = "http://127.0.0.1:8000/cart/"
                }
            })
        }
    })
})