
var updateBtns = document.getElementsByClassName('update-cart')


for (var i = 0; i < updateBtns.length; i++) {

  updateBtns[i].addEventListener('click', function(e) {

    var productId = this.dataset.product
    var action = this.dataset.action
    console.log('productId:', productId, 'action:', action)

   
    if (user === 'AnonymousUser') {
      addCookieItem(productId, action);
    } else {
       updateUserOrder(productId, action);
      
    }

  });
}


function updateUserOrder(productId, action) {
  console.log('User is logged in, sending data...')

  var url = '/update_item/'

  fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrftoken,
    },
    body: JSON.stringify({ 'productId': productId, 'action': action })
  })
  .then((response) => {
    return response.json()
  })
  .then((data) => {
    console.log('data:', data)
    location.reload()
  })
}

//addtioinal

function getCookie(name) {
    let cookieArr = document.cookie.split(";");
    for (let i = 0; i < cookieArr.length; i++) {
        let cookiePair = cookieArr[i].split("=");
        if (name === cookiePair[0].trim()) {
            return decodeURIComponent(cookiePair[1]);
        }
    }
    return null;
}

let cart = JSON.parse(getCookie('cart') || '{}');

function addCookieItem(productId, action) {
    console.log("User not logged in...")

    if (action == 'add') {
        if (cart[productId] == undefined) {
            cart[productId] = {'quantity': 1};
        } else {
            cart[productId]['quantity'] += 1;
        }
    }

    if (action == 'remove') {
        cart[productId]['quantity'] -= 1;

        if (cart[productId]['quantity'] <= 0) {
            delete cart[productId];
        }
    }

    console.log('Cart:', cart);
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/";

    location.reload();
}

function addToCart(productId, btn) {
    let quantity = 1;
    if (btn) {
        quantity = btn.closest('form').querySelector('input[name="quantity"]').value;
    } else {
        quantity = document.getElementById('quantity').value;
    }
    fetch("{% url 'ecommerce:update_item' %}", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify({
            productId: productId,
            action: "add",
            quantity: parseInt(quantity)
        })
    })
    .then(response => response.json().then(data => ({status: response.status, body: data})))
    .then(res => {
        if (res.status === 400 && res.body.error) {
            alert(res.body.error);
        } else {
            location.reload();
        }
    });
}