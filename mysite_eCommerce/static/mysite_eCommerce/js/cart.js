
var updatebtn = document.getElementsByClassName('update-cart')

for (var i=0; i< updatebtn.length;i++){
        updatebtn[i].addEventListener('click', function(){
            var pId =  this.dataset.product
            var action =  this.dataset.action
            if(user === 'AnonymousUser'){
            window.location.href = "/login/";
            alert("User not logged in")
            }
            else{
            updateUserOrder(pId,action)
            }

        })
}

function updateUserOrder(productId ,action){
       $.ajax({

            type: 'POST',
            url: "/updateitem/",

            data: {pid: productId,
            action:action},

            success: function (response) {

                // if not valid user, alert the user
                location.reload()

            },

            error: function (response) {

                alert("Error Occured!!!")

            }

        })
}