from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from .models import Wheel, Nav, Mustbuy, Shop, MainShow, FoodTypes, Goods, User, Cart
from .models import Order
from .forms.login import LoginForm
import time
import os
import random
# Create your views here.

# 主页
def home(request):
    wheelList = Wheel.objects.all()
    navList  = Nav.objects.all()
    mustbuyList = Mustbuy.objects.all()

    shopList = Shop.objects.all()
    shop1 = shopList[0]
    shop2 = shopList[1:3]
    shop3 = shopList[3:7]
    shop4 = shopList[7:]

    mainList = MainShow.objects.all()

    return render(request, 'axf/home.html', {"title": "主页", "wheelList": wheelList, "navList": navList,
                                             "mustbuyList": mustbuyList, "shop1": shop1, "shop2": shop2,
                                             "shop3": shop3, "shop4": shop4, "mainList": mainList, })


# 闪送超市
def market(request, categoryid, childcid, sortid):
    leftNavList = FoodTypes.objects.all()

    if childcid == "0":
        goodsList = Goods.objects.filter(categoryid=categoryid)
    else:
        goodsList = Goods.objects.filter(categoryid=categoryid, childcid=childcid)

    # 排序
    if sortid == '1':
        productList = goodsList.order_by("productnum")
    elif sortid == '2':
        productList = goodsList.order_by("price")
    elif sortid == '3':
        productList = goodsList.order_by("-price")

    group = leftNavList.get(typeid=categoryid)
    childList = []
    # 全部分类:0#进口水果:103534#国产水果:103533
    childnames = group.childtypenames
    arr1 = childnames.split("#")
    for str in  arr1:
        # 全部分类:0
        arr2 = str.split(":")
        obj = {"childName": arr2[0], "childId": arr2[1]}
        childList.append(obj)

    usertoken = request.session.get("usertoken")
    if usertoken != None:
        cartlist = []
        user = User.objects.get(userToken=usertoken)
        cartlist = Cart.objects.filter(userAccount=user.userAccount)
        for p in goodsList:
            for c in cartlist:
                if p.productid == c.productid:
                    p.num = c.productnum
                    print(p.num)
                    continue

    return render(request, 'axf/market.html', {"title": "闪送超市", "leftNavList": leftNavList,
                                               "goodsList": goodsList,"childList": childList,
                                               "categoryid": categoryid, "childcid": childcid, })

# 改变所购商品数量并添加到购物车
def changecart(request, flag):
    usertoken = request.session.get("usertoken")
    if usertoken == None:
        # 用户未登录
        return JsonResponse({"data": -1, "status": "error"})
    # 获取当前操作的商品以及用户
    productid = request.POST.get("productid")
    product = Goods.objects.get(productid=productid)
    user = User.objects.get(userToken=usertoken)
    # 增加商品数量
    if flag == "0":
        # 判断商品库存数
        if product.storenums == 0:
            return JsonResponse({"data": -2, "status": "error"})
        carts = Cart.objects.filter(userAccount = user.userAccount)
        c = None
        if carts.count() == 0:
            # 直接增加一条订单
            c = Cart.createcart(user.userAccount, productid, 1, product.price, True,
                                product.productimg, product.productlongname, False)
            c.save()
        else:
            try:
                c = carts.get(productid = productid)
                # 修改数量和价格
                c.productnum += 1
                c.productprice = "%.2f" % (float(product.price) * c.productnum)
                c.save()
            except Cart.DoesNotExist as e:
                # 直接增加一条订单
                c = Cart.createcart(user.userAccount, productid, 1, product.price, True,
                                    product.productimg, product.productlongname, False)
                c.save()
        sumprice = 0
        for item in carts:
            if item.isChose:
                sumprice += float(item.productprice)
        sumprice = "%.2f" % (sumprice)
        # 库存减一
        product.storenums -= 1
        product.save()
        return JsonResponse({"data": c.productnum, "sumprice": sumprice, "status": "success",
                             "price": c.productprice, })

    # 减少商品数量
    elif flag == "1":
        carts = Cart.objects.filter(userAccount=user.userAccount)
        c = None
        if carts.count() == 0:
            return JsonResponse({"data": -2, "status": "error"})
        else:
            try:
                c = carts.get(productid=product.productid)
                # 修改数量和价格
                c.productnum -= 1
                c.productprice = "%.2f" % (float(product.price) * c.productnum)
                if c.productnum == 0:
                    c.delete()
                else:
                    c.save()
            except Cart.DoesNotExist as e:
                return JsonResponse({"data": -2, "status": "error"})
        sumprice = 0
        for item in carts:
            if item.isChose:
                sumprice += float(item.productprice)
        sumprice = "%.2f" % (sumprice)
        product.storenums += 1
        product.save()
        return JsonResponse({"data": c.productnum, "sumprice": sumprice, "status": "success",
                             "price": c.productprice, })
    elif flag == "2":
        carts = Cart.objects.filter(userAccount=user.userAccount)
        c = carts.get(productid=productid)
        c.isChose = not c.isChose
        c.save()
        sumprice = 0
        str = ""
        if c.isChose:
            str = "√"
        for c in carts:
            if c.isChose:
                sumprice += float(c.productprice)
        sumprice = "%.2f" % (sumprice)
        return JsonResponse({"data": str, "sumprice": sumprice, "status": "success"})
    elif flag == "3":
        pass


# 购物车
def cart(request):
    cartslist = []
    sumprice = 0.0
    str = ""
    usertoken = request.session.get("usertoken")
    if usertoken == None:
        return redirect('/login/')
    user = User.objects.get(userToken=usertoken)
    cartslist = Cart.objects.filter(userAccount=user.userAccount)
    countnum = 0
    num = cartslist.count()
    for c in cartslist:
        if c.isChose:
            countnum += 1
            sumprice += float(c.productprice)
    if countnum == num:
        str = "√"
    sumprice = "%.2f" % (sumprice)
    return render(request, 'axf/cart.html', {"title": "购物车", "cartslist": cartslist,
                                             "consignee": user.userName, "phone": user.userPhone,
                                             "address": user.userAdderss, "sumprice": sumprice,
                                             "str": str, })

# 下订单
def saveorder(request):
    usertoken = request.session.get("usertoken")
    user = User.objects.get(userToken=usertoken)
    carts = Cart.objects.filter(userAccount=user.userAccount, isChose=True)
    if carts.count() == 0:
        return JsonResponse({"data": -1, "status": "error"})
    oid = str("%d" % (time.time() + random.randrange(1, 10000)))
    o = Order.createorder(oid, user.userAccount, 0)
    o.save()
    for c in carts:
        c.isDelete = True
        c.orderid = oid
        c.save()
    return JsonResponse({"status": "success"})


# 我的
def mine(request):
    username = request.session.get("username", "未登录")
    return render(request, 'axf/mine.html', {"title": "我的", "username": username, })

# 登录
def login(request):
    if request.method == "POST":
        f = LoginForm(request.POST)
        if f.is_valid():
            # 信息格式没多大问题，验证账号和密码的正确性
            name = f.cleaned_data["username"]
            pswd = f.cleaned_data["passwd"]
            try:
                user = User.objects.get(userAccount = name)
                if user.userPasswd != pswd:
                    return render(request, 'axf/login.html', {"error2": "用户名或密码错误！",
                                                              "title": "登录", "form": f,
                                                              "error": f.errors, })
            except User.DoesNotExist as e:
                return render(request, 'axf/login.html', {"error2": "该用户不存在！", "title": "登录",
                                                          "form": f, "error": f.errors, })

            # 登陆成功
            user.userToken = str(time.time() + random.randrange(0, 10000))
            user.save()
            request.session["username"] = user.userName
            request.session["usertoken"] = user.userToken
            request.session.set_expiry(0)
            return redirect('/mine/')
        else:
            return render(request, 'axf/login.html', {"title": "登录", "form": f, "error": f.errors, })
    else:
        f = LoginForm()
        return render(request, 'axf/login.html', {"title": "登录", "form": f, })

from django.contrib.auth import logout
# 注销登录
def quit(request):
    logout(request)
    return redirect('/mine/')

# 注册账户
def register(request):
    if request.method == "POST":
        userAccount = request.POST.get("userAccount")
        userPasswd = request.POST.get("userPasswd")
        userName = request.POST.get("userName")
        userPhone = request.POST.get("userPhone")
        userAdderss = request.POST.get("userAdderss")
        userRank = 0
        userToken = str(time.time() + random.randrange(0, 10000))
        userImg = os.path.join(settings.MEDIA_ROOT, userAccount + ".png")
        f = request.FILES["userImg"]
        with open(userImg, "wb") as fp:
            for data in f.chunks():
                fp.write(data)
        user = User.createuser(userAccount, userPasswd, userName, userPhone, userAdderss,
                               userImg, userRank, userToken)
        user.save()
        request.session["username"] = userName
        request.session["usertoken"] = userToken
        request.session.set_expiry(0)
        return redirect('/mine/')
    else:
        return render(request, 'axf/register.html', {"title": "注册"})

# 注册时，检测用户是否已被注册
def checkuserid(request):
    userid = request.POST.get("userid")
    try:
        user = User.objects.get(userAccount = userid)
        return JsonResponse({"data":"该用户已经被注册", "status": "error", })
    except User.DoesNotExist as e:
        return JsonResponse({"data": "可以注册", "status": "success"})